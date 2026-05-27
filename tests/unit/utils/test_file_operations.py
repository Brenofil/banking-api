"""
Unit tests for FileOperations class
"""

import os
import tempfile
import shutil
from io import BytesIO
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
import pandas as pd

from app.constants.files import FileConstants
from app.utils.file_operations import FileOperations


class TestFileOperations:
    """
    Test Suite for FileOperations class
    """

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing"""
        temp_path = tempfile.mkdtemp()
        yield temp_path
        # Cleanup after test
        if os.path.exists(temp_path):
            shutil.rmtree(temp_path)

    @pytest.fixture
    def file_ops(self, temp_dir):
        """Create FileOperations instance with temp directory"""
        return FileOperations(base_directory=temp_dir)

    def test_init_with_base_directory(self, temp_dir):
        """Test initialization with explicit base directory"""
        ops = FileOperations(base_directory=temp_dir)
        assert ops.base_directory == temp_dir
        assert os.path.exists(temp_dir)

    def test_init_without_base_directory(self):
        """Test initialization without base directory (uses default)"""
        with patch.dict(os.environ, {}, clear=True):
            ops = FileOperations()
            assert ops.base_directory == "files"
            # Cleanup
            if os.path.exists("files"):
                shutil.rmtree("files")

    def test_init_with_env_variable(self, temp_dir):
        """Test initialization with FILE_LOCATION environment variable"""
        with patch.dict(os.environ, {"FILE_LOCATION": temp_dir}):
            ops = FileOperations()
            assert ops.base_directory == temp_dir

    def test_create_with_string_content(self, file_ops):
        """Test creating file with string content"""
        result = file_ops.create(filename="test.txt", content="Hello World")
        assert os.path.exists(result)
        assert file_ops.read(filename="test.txt", mode="r") == "Hello World"

    def test_create_with_bytes_content(self, file_ops):
        """Test creating file with bytes content"""
        content = b"Binary content"
        result = file_ops.create(filename="test.bin", content=content)
        assert os.path.exists(result)
        assert file_ops.read(filename="test.bin") == content

    def test_create_with_bytesio_content(self, file_ops):
        """Test creating file with BytesIO content"""
        content = BytesIO(b"BytesIO content")
        result = file_ops.create(filename="test.dat", content=content)
        assert os.path.exists(result)
        assert file_ops.read(filename="test.dat") == b"BytesIO content"

    def test_create_with_dataframe(self, file_ops):
        """Test creating Excel file with single DataFrame"""
        df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
        result = file_ops.create(filename="test.xlsx", content=df)
        assert os.path.exists(result)
        assert result.endswith(".xlsx")

    def test_create_with_dataframe_list(self, file_ops):
        """Test creating Excel file with list of DataFrames"""
        df1 = pd.DataFrame({"A": [1, 2]})
        df2 = pd.DataFrame({"B": [3, 4]})
        result = file_ops.create(filename="test_multi.xlsx", content=[df1, df2])
        assert os.path.exists(result)

    def test_create_with_subdirectory(self, file_ops, temp_dir):
        """Test creating file in subdirectory"""
        subdir_path = os.path.join(temp_dir, "subdir")
        result = file_ops.create(
            filename="test.txt", content="test", directory=subdir_path
        )
        assert os.path.exists(result)
        assert "subdir" in result

    def test_create_without_filename_raises_error(self, file_ops):
        """Test that creating without filename raises ValueError"""
        with pytest.raises(ValueError, match="filename parameter is required"):
            file_ops.create(content="test")

    def test_create_without_content_raises_error(self, file_ops):
        """Test that creating without content raises ValueError"""
        with pytest.raises(ValueError, match="content parameter is required"):
            file_ops.create(filename="test.txt")

    def test_create_file_exists_without_overwrite(self, file_ops):
        """Test that creating existing file without overwrite raises FileExistsError"""
        file_ops.create(filename="test.txt", content="test")
        with pytest.raises(FileExistsError, match="File already exists"):
            file_ops.create(filename="test.txt", content="test2")

    def test_create_file_exists_with_overwrite(self, file_ops):
        """Test that creating existing file with overwrite succeeds"""
        file_ops.create(filename="test.txt", content="test1")
        result = file_ops.create(filename="test.txt", content="test2", overwrite=True)
        assert os.path.exists(result)
        assert file_ops.read(filename="test.txt", mode="r") == "test2"

    def test_create_with_unsupported_content_type(self, file_ops):
        """Test that creating with unsupported content type raises IOError"""
        with pytest.raises(IOError, match="Failed to create file"):
            file_ops.create(filename="test.txt", content=12345)

    def test_create_io_error(self, file_ops):
        """Test that IOError is raised when file creation fails"""
        with patch("builtins.open", side_effect=PermissionError("No permission")):
            with pytest.raises(IOError, match="Failed to create file"):
                file_ops.create(filename="test.txt", content="test")

    def test_read_existing_file(self, file_ops):
        """Test reading existing file"""
        file_ops.create(filename="test.txt", content="Hello")
        content = file_ops.read(filename="test.txt", mode="r")
        assert content == "Hello"

    def test_read_binary_mode(self, file_ops):
        """Test reading file in binary mode"""
        file_ops.create(filename="test.bin", content=b"Binary")
        content = file_ops.read(filename="test.bin", mode="rb")
        assert content == b"Binary"

    def test_read_without_filename_raises_error(self, file_ops):
        """Test that reading without filename raises ValueError"""
        with pytest.raises(ValueError, match="filename parameter is required"):
            file_ops.read()

    def test_read_nonexistent_file_raises_error(self, file_ops):
        """Test that reading nonexistent file raises FileNotFoundError"""
        with pytest.raises(FileNotFoundError, match="File not found"):
            file_ops.read(filename="nonexistent.txt")

    def test_read_io_error(self, file_ops):
        """Test that IOError is raised when file reading fails"""
        file_ops.create(filename="test.txt", content="test")
        with patch("builtins.open", side_effect=PermissionError("No permission")):
            with pytest.raises(IOError, match="Failed to read file"):
                file_ops.read(filename="test.txt")

    def test_update_existing_file(self, file_ops):
        """Test updating existing file"""
        file_ops.create(filename="test.txt", content="Original")
        result = file_ops.update(filename="test.txt", content="Updated")
        assert os.path.exists(result)
        assert file_ops.read(filename="test.txt", mode="r") == "Updated"

    def test_update_without_filename_raises_error(self, file_ops):
        """Test that updating without filename raises ValueError"""
        with pytest.raises(ValueError, match="filename parameter is required"):
            file_ops.update(content="test")

    def test_update_nonexistent_file_raises_error(self, file_ops):
        """Test that updating nonexistent file raises FileNotFoundError"""
        with pytest.raises(FileNotFoundError, match="File not found"):
            file_ops.update(filename="nonexistent.txt", content="test")

    def test_delete_existing_file(self, file_ops):
        """Test deleting existing file"""
        file_ops.create(filename="test.txt", content="test")
        result = file_ops.delete(filename="test.txt")
        assert result is True
        assert not file_ops.exists(filename="test.txt")

    def test_delete_without_filename_raises_error(self, file_ops):
        """Test that deleting without filename raises ValueError"""
        with pytest.raises(ValueError, match="filename parameter is required"):
            file_ops.delete()

    def test_delete_nonexistent_file_raises_error(self, file_ops):
        """Test that deleting nonexistent file raises FileNotFoundError"""
        with pytest.raises(FileNotFoundError, match="File not found"):
            file_ops.delete(filename="nonexistent.txt")

    def test_delete_io_error(self, file_ops):
        """Test that IOError is raised when file deletion fails"""
        file_ops.create(filename="test.txt", content="test")
        with patch("os.remove", side_effect=PermissionError("No permission")):
            with pytest.raises(IOError, match="Failed to delete file"):
                file_ops.delete(filename="test.txt")

    def test_exists_returns_true_for_existing_file(self, file_ops):
        """Test that exists returns True for existing file"""
        file_ops.create(filename="test.txt", content="test")
        assert file_ops.exists(filename="test.txt") is True

    def test_exists_returns_false_for_nonexistent_file(self, file_ops):
        """Test that exists returns False for nonexistent file"""
        assert file_ops.exists(filename="nonexistent.txt") is False

    def test_exists_returns_false_without_filename(self, file_ops):
        """Test that exists returns False when filename is not provided"""
        assert file_ops.exists() is False

    def test_list_files_in_directory(self, file_ops):
        """Test listing files in directory"""
        file_ops.create(filename="file1.txt", content="test1")
        file_ops.create(filename="file2.txt", content="test2")
        files = file_ops.list()
        assert len(files) == 2
        assert "file1.txt" in files
        assert "file2.txt" in files

    def test_list_files_with_pattern(self, file_ops):
        """Test listing files with pattern filter"""
        file_ops.create(filename="file1.txt", content="test1")
        file_ops.create(filename="file2.csv", content="test2")
        files = file_ops.list(pattern="*.txt")
        assert len(files) == 1
        assert "file1.txt" in files

    def test_list_files_recursive(self, file_ops, temp_dir):
        """Test listing files recursively"""
        file_ops.create(filename="file1.txt", content="test1")

        subdir_path = os.path.join(temp_dir, "subdir")
        file_ops.create(filename="file2.txt", content="test2", directory=subdir_path)

        files = file_ops.list(recursive=True)
        assert len(files) == 2
        assert "file1.txt" in files
        assert os.path.join("subdir", "file2.txt") in files

    def test_list_files_in_subdirectory(self, file_ops, temp_dir):
        """Test listing files in subdirectory"""
        subdir_path = os.path.join(temp_dir, "subdir")

        file_ops.create(filename="file1.txt", content="test1", directory=subdir_path)

        files = file_ops.list(directory=subdir_path)
        assert len(files) == 1
        assert files[0].endswith(os.path.join("subdir", "file1.txt"))

    def test_list_files_io_error(self, file_ops):
        """Test that IOError is raised when listing fails"""
        with patch("glob.glob", side_effect=PermissionError("No permission")):
            with pytest.raises(IOError, match="Failed to list files"):
                file_ops.list()

    def test_validate_size_with_valid_content(self, file_ops):
        """Test validate_size with valid content"""
        content = b"Valid content"
        assert file_ops.validate_size(content=content) is True

    def test_validate_size_with_empty_content(self, file_ops):
        """Test validate_size with empty content raises ValueError (falsy check)"""
        content = b""
        with pytest.raises(ValueError, match="content parameter is required"):
            file_ops.validate_size(content=content)

    def test_validate_size_with_oversized_content(self, file_ops):
        """Test validate_size with oversized content"""
        # Create content larger than MAX_FILE_SIZE_BYTES
        content = b"x" * (FileConstants.MAX_FILE_SIZE_BYTES + 1)
        assert file_ops.validate_size(content=content) is False

    def test_validate_size_without_content_raises_error(self, file_ops):
        """Test that validate_size without content raises ValueError"""
        with pytest.raises(ValueError, match="content parameter is required"):
            file_ops.validate_size()

    def test_validate_size_with_none_content_raises_error(self, file_ops):
        """Test that validate_size with None content raises ValueError"""
        with pytest.raises(ValueError, match="content parameter is required"):
            file_ops.validate_size(content=None)

    def test_max_file_size_from_env(self):
        """Test that MAX_FILE_SIZE_MB is read from environment variable"""
        # Need to reload the module to pick up the new env variable
        import importlib
        import app.constants.files

        with patch.dict(os.environ, {"MAX_FILE_SIZE_MB": "20"}):
            # Reload module to pick up new environment variable
            importlib.reload(app.constants.files)
            from app.constants.files import FileConstants as ReloadedFileConst

            try:
                assert ReloadedFileConst.MAX_FILE_SIZE_MB == 20
                assert ReloadedFileConst.MAX_FILE_SIZE_BYTES == 20 * 1024 * 1024
            finally:
                # Reload again to restore original state
                importlib.reload(app.constants.files)

    def test_write_excel_io_error(self, file_ops):
        """Test that _write_excel raises IOError on failure"""
        df = pd.DataFrame({"A": [1, 2]})
        with patch("pandas.ExcelWriter", side_effect=Exception("Write failed")):
            with pytest.raises(IOError, match="Failed to write Excel file"):
                file_ops._write_excel("test.xlsx", df)
