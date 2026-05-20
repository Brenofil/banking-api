"""
Unit tests for FileExtension enum
"""

import pytest
from app.enums.file_extensions import FileExtension


class TestFileExtensions:
    """Test suite for FileExtension enum"""

    def test_enum_values_exist(self):
        """Test that all expected enum values exist"""
        assert FileExtension.PDF == ".pdf"
        assert FileExtension.CSV == ".csv"
        assert FileExtension.XLSX == ".xlsx"
        assert FileExtension.XLS == ".xls"
        assert FileExtension.DOCX == ".docx"
        assert FileExtension.DOC == ".doc"
        assert FileExtension.TXT == ".txt"
        assert FileExtension.JSON == ".json"
        assert FileExtension.XML == ".xml"

    def test_enum_members_count(self):
        """Test that enum has exactly 3 members"""
        assert len(FileExtension.__members__) == 9

    def test_enum_member_names(self):
        """Test that all expected member names exist"""
        member_names = list(FileExtension.__members__.keys())
        assert "PDF" in member_names
        assert "CSV" in member_names
        assert "XLSX" in member_names
        assert "XLS" in member_names
        assert "DOCX" in member_names
        assert "DOC" in member_names
        assert "TXT" in member_names
        assert "JSON" in member_names
        assert "XML" in member_names

    def test_enum_is_string_type(self):
        """Test that enum values are strings"""
        assert isinstance(FileExtension.PDF.value, str)
        assert isinstance(FileExtension.CSV.value, str)
        assert isinstance(FileExtension.XLSX.value, str)
        assert isinstance(FileExtension.XLS.value, str)
        assert isinstance(FileExtension.DOCX.value, str)
        assert isinstance(FileExtension.DOC.value, str)
        assert isinstance(FileExtension.TXT.value, str)
        assert isinstance(FileExtension.JSON.value, str)
        assert isinstance(FileExtension.XML.value, str)

    def test_enum_comparison(self):
        """Test enum value comparison"""
        assert FileExtension.PDF == FileExtension.PDF
        assert FileExtension.CSV != FileExtension.PDF
        assert FileExtension.PDF != FileExtension.DOCX

    @pytest.mark.parametrize(
        "extension,expected",
        [
            (FileExtension.PDF, ".pdf"),
            (FileExtension.CSV, ".csv"),
            (FileExtension.XLSX, ".xlsx"),
            (FileExtension.XLS, ".xls"),
            (FileExtension.DOCX, ".docx"),
            (FileExtension.DOC, ".doc"),
            (FileExtension.TXT, ".txt"),
            (FileExtension.JSON, ".json"),
            (FileExtension.XML, ".xml"),
        ],
    )
    def test_enum_value_mapping(self, extension, expected):
        """Test that enum values map correctly"""
        assert extension.value == expected
        # str() returns the enum name format, not the value
        assert str(extension) == f"FileExtension.{extension.name}"

    def test_enum_iteration(self):
        """Test iterating over enum members"""
        extensions = [extension for extension in FileExtension]
        assert len(extensions) == 9
        assert FileExtension.PDF in extensions
        assert FileExtension.CSV in extensions
        assert FileExtension.DOCX in extensions

    def test_enum_access_by_name(self):
        """Test accessing enum by member name"""
        assert FileExtension["PDF"] == FileExtension.PDF
        assert FileExtension["XLSX"] == FileExtension.XLSX
        assert FileExtension["DOCX"] == FileExtension.DOCX

    def test_enum_access_by_value(self):
        """Test accessing enum by value"""
        assert FileExtension(".pdf") == FileExtension.PDF
        assert FileExtension(".doc") == FileExtension.DOC
        assert FileExtension(".json") == FileExtension.JSON

    def test_enum_invalid_access_raises_error(self):
        """Test that accessing invalid enum raises error"""
        with pytest.raises(ValueError):
            FileExtension("Invalid")

        with pytest.raises(KeyError):
            FileExtension["INVALID"]

    # Tests for get_extension_to_type_map method
    def test_get_extension_to_type_map(self) -> None:
        extension_list = FileExtension.__members__.values()
        type_map = FileExtension.get_extension_to_type_map()

        assert len(type_map.keys()) == 9

        for extension in extension_list:
            assert extension in type_map

    # Tests for from_file_type method
    @pytest.mark.parametrize(
        "file_type, expected",
        [
            ("pdf", ".pdf"),
            ("csv", ".csv"),
            ("xlsx", ".xlsx"),
            ("xls", ".xls"),
            ("docx", ".docx"),
            ("doc", ".doc"),
            ("txt", ".txt"),
            ("json", ".json"),
            ("xml", ".xml"),
            ("xlsx", ".xlsx"),
        ],
    )
    def test_from_file_type(self, file_type, expected) -> None:
        assert FileExtension.from_file_type(file_type) == expected

    def test_from_file_type_error(self) -> None:
        with pytest.raises(ValueError):
            FileExtension.from_file_type("Invalid")

    # Tests for from_string method
    @pytest.mark.parametrize(
        "extension, expected",
        [
            ("PDF", ".pdf"),
            ("CSV", ".csv"),
            ("XLsX", ".xlsx"),
            ("xLs", ".xls"),
            ("DocX", ".docx"),
            ("DOC", ".doc"),
            ("TxT", ".txt"),
            ("JSON", ".json"),
            ("XmL", ".xml"),
            ("XLSX", ".xlsx"),
        ],
    )
    def test_from_string(self, extension, expected) -> None:
        assert FileExtension.from_string(extension) == expected

    def test_from_string_error(self) -> None:
        with pytest.raises(ValueError):
            FileExtension.from_string("Invalid")

    # Tests for get_all_extensions method
    def test_get_all_extensions(self) -> None:
        all_extensions = FileExtension.get_all_extensions()
        extension_list = FileExtension.__members__.values()

        assert len(all_extensions) == 9

        for extension in extension_list:
            assert extension in all_extensions

    # Tests for is_supported method
    @pytest.mark.parametrize(
        "extension,expected",
        [
            (".mkv", False),
            (".mp4", False),
            (FileExtension.PDF, True),
            (FileExtension.CSV, True),
            (FileExtension.XLSX, True),
            (FileExtension.XLS, True),
        ],
    )
    def test_is_supported(self, extension, expected) -> None:
        assert FileExtension.is_supported(extension) == expected
