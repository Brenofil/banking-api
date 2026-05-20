"""
File Operations utility implementing CRUD interface for local file system operations.
"""

import os
import glob
from pathlib import Path
from typing import Any, Optional, Union, List
from io import BytesIO
from fastapi import UploadFile
import pandas as pd

from app.interfaces.crud_interface import CrudInterface
from app.utils.logger import LoggerService


class FileOperations(CrudInterface):
    """
    File operations implementation of CRUD interface.

    Handles local file system operations including creating, reading,
    updating, and deleting files. Supports various file types including
    Excel files for DataFrame exports.
    """

    name: str = "File Operations"
    logger = LoggerService().get_logger(name)

    # Get max file size from environment variable (default: 10 MB)
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
    MAX_FILE_SIZE_BYTES: int = MAX_FILE_SIZE_MB * 1024 * 1024

    def __init__(self, base_directory: Optional[str] = None):
        """
        Initialize FileOperations with a base directory.

        Args:
            base_directory: Base directory for file operations.
                          If None, uses FILE_LOCATION from environment or current directory.
        """
        if base_directory is None:
            # Try to get from environment variable
            base_directory = os.getenv("FILE_LOCATION")

            # If not set, default to "files" directory
            if not base_directory:
                base_directory = "files"
                self.logger.info(
                    "FILE_LOCATION not set, using default 'files' directory"
                )

        self.base_directory = base_directory

        # Create base directory if it doesn't exist
        os.makedirs(self.base_directory, exist_ok=True)
        self.logger.info(
            f"FileOperations initialized with base directory: {self.base_directory}"
        )

    def create(self, **kwargs) -> str:
        """
        Create a new file.

        Args:
            **kwargs: Required parameters:
                - filename (str): Name of the file to create
                - content (Union[bytes, str, BytesIO, pd.DataFrame, list[pd.DataFrame]]): File content
                Optional parameters:
                - directory (str): Subdirectory within base_directory
                - mode (str): File write mode (default: 'wb' for bytes, 'w' for str)
                - overwrite (bool): Whether to overwrite existing file (default: False)

        Returns:
            str: Full path to the created file

        Raises:
            ValueError: If required parameters are missing
            FileExistsError: If file exists and overwrite=False
            IOError: If file creation fails
        """
        filename = kwargs.get("filename")
        content = kwargs.get("content")
        directory = kwargs.get("directory", "")
        overwrite = kwargs.get("overwrite", False)

        if not filename:
            raise ValueError("filename parameter is required")
        if content is None:
            raise ValueError("content parameter is required")

        # Build full path
        full_directory = os.path.join(self.base_directory, directory)
        os.makedirs(full_directory, exist_ok=True)

        file_path = os.path.join(full_directory, filename)

        # Check if file exists
        if os.path.exists(file_path) and not overwrite:
            raise FileExistsError(f"File already exists: {file_path}")

        try:
            # Handle DataFrame or list of DataFrames (export to Excel)
            if isinstance(content, pd.DataFrame) or (
                isinstance(content, list)
                and content
                and isinstance(content[0], pd.DataFrame)
            ):
                self._write_excel(file_path, content)
            # Handle BytesIO
            elif isinstance(content, BytesIO):
                with open(file_path, "wb") as f:
                    f.write(content.getvalue())
            # Handle bytes
            elif isinstance(content, bytes):
                with open(file_path, "wb") as f:
                    f.write(content)
            # Handle string
            elif isinstance(content, str):
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
            else:
                raise ValueError(f"Unsupported content type: {type(content)}")

            self.logger.info(f"File created successfully: {file_path}")
            return file_path

        except Exception as e:
            self.logger.error(f"Failed to create file {file_path}: {str(e)}")
            raise IOError(f"Failed to create file: {str(e)}")

    def read(self, **kwargs) -> Any:
        """
        Read content from an existing file.

        Args:
            **kwargs: Required parameters:
                - filename (str): Name of the file to read
                Optional parameters:
                - directory (str): Subdirectory within base_directory
                - mode (str): File read mode (default: 'rb')
                - encoding (str): Text encoding (default: 'utf-8' for text mode)

        Returns:
            Any: File content (bytes or str depending on mode)

        Raises:
            ValueError: If required parameters are missing
            FileNotFoundError: If file doesn't exist
            IOError: If file reading fails
        """
        filename = kwargs.get("filename")
        directory = kwargs.get("directory", "")
        mode = kwargs.get("mode", "rb")
        encoding = kwargs.get("encoding", "utf-8")

        if not filename:
            raise ValueError("filename parameter is required")

        # Build full path
        file_path = os.path.join(self.base_directory, directory, filename)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            if "b" in mode:
                with open(file_path, mode) as f:
                    content = f.read()
            else:
                with open(file_path, mode, encoding=encoding) as f:
                    content = f.read()

            self.logger.info(f"File read successfully: {file_path}")
            return content

        except Exception as e:
            self.logger.error(f"Failed to read file {file_path}: {str(e)}")
            raise IOError(f"Failed to read file: {str(e)}")

    def update(self, **kwargs) -> str:
        """
        Update an existing file with new content.

        Args:
            **kwargs: Same as create() method

        Returns:
            str: Full path to the updated file

        Raises:
            ValueError: If required parameters are missing
            FileNotFoundError: If file doesn't exist
            IOError: If file update fails
        """
        filename = kwargs.get("filename")
        directory = kwargs.get("directory", "")

        if not filename:
            raise ValueError("filename parameter is required")

        # Build full path
        file_path = os.path.join(self.base_directory, directory, filename)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        # Use create with overwrite=True
        kwargs["overwrite"] = True
        return self.create(**kwargs)

    def delete(self, **kwargs) -> bool:
        """
        Delete an existing file.

        Args:
            **kwargs: Required parameters:
                - filename (str): Name of the file to delete
                Optional parameters:
                - directory (str): Subdirectory within base_directory

        Returns:
            bool: True if deletion was successful

        Raises:
            ValueError: If required parameters are missing
            FileNotFoundError: If file doesn't exist
            IOError: If file deletion fails
        """
        filename = kwargs.get("filename")
        directory = kwargs.get("directory", "")

        if not filename:
            raise ValueError("filename parameter is required")

        # Build full path
        file_path = os.path.join(self.base_directory, directory, filename)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            os.remove(file_path)
            self.logger.info(f"File deleted successfully: {file_path}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to delete file {file_path}: {str(e)}")
            raise IOError(f"Failed to delete file: {str(e)}")

    def exists(self, **kwargs) -> bool:
        """
        Check if a file exists.

        Args:
            **kwargs: Required parameters:
                - filename (str): Name of the file to check
                Optional parameters:
                - directory (str): Subdirectory within base_directory

        Returns:
            bool: True if file exists, False otherwise
        """
        filename = kwargs.get("filename")
        directory = kwargs.get("directory", "")

        if not filename:
            return False

        # Build full path
        file_path = os.path.join(self.base_directory, directory, filename)
        return os.path.exists(file_path)

    def list(self, **kwargs) -> list[str]:
        """
        List files in the storage location.

        Args:
            **kwargs: Optional parameters:
                - directory (str): Subdirectory within base_directory
                - pattern (str): Glob pattern to filter files (e.g., "*.xlsx")
                - recursive (bool): Whether to search recursively (default: False)

        Returns:
            list[str]: List of filenames (relative to base_directory)

        Raises:
            IOError: If listing fails
        """
        directory = kwargs.get("directory", "")
        pattern = kwargs.get("pattern", "*")
        recursive = kwargs.get("recursive", False)

        try:
            # Build search path
            search_dir = os.path.join(self.base_directory, directory)

            if recursive:
                search_pattern = os.path.join(search_dir, "**", pattern)
                files = glob.glob(search_pattern, recursive=True)
            else:
                search_pattern = os.path.join(search_dir, pattern)
                files = glob.glob(search_pattern)

            # Return relative paths
            relative_files = [
                os.path.relpath(f, self.base_directory)
                for f in files
                if os.path.isfile(f)
            ]

            self.logger.info(f"Listed {len(relative_files)} files in {search_dir}")
            return relative_files

        except Exception as e:
            self.logger.error(f"Failed to list files: {str(e)}")
            raise IOError(f"Failed to list files: {str(e)}")

    def _write_excel(
        self, file_path: str, dataframes: Union[pd.DataFrame, List[pd.DataFrame]]
    ) -> None:
        """
        Write DataFrame(s) to Excel file.

        Args:
            file_path: Full path to the Excel file
            dataframes: Single DataFrame or list of DataFrames

        Raises:
            IOError: If Excel writing fails
        """
        try:
            with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
                if isinstance(dataframes, list):
                    # Multiple DataFrames - write each to a separate sheet
                    for i, df in enumerate(dataframes, start=1):
                        sheet_name = f"Table_{i}"
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
                    self.logger.info(
                        f"Wrote {len(dataframes)} DataFrames to Excel: {file_path}"
                    )
                else:
                    # Single DataFrame
                    dataframes.to_excel(writer, sheet_name="Table_1", index=False)
                    self.logger.info(f"Wrote single DataFrame to Excel: {file_path}")

        except Exception as e:
            raise IOError(f"Failed to write Excel file: {str(e)}")

    def validate_size(self, content: bytes | None = None) -> bool:
        """
        Validates a file size, returns False for either empty or undefined Files

        Args:
            **kwargs: Required parameters:
                -content (bytes): the content of a file. Default is None

        Returns:
            bool: True if the file size is valid, False otherwise
        """

        if not content:
            self.logger.error("Should not measure undefined content")
            raise ValueError("content parameter is required")

        size: int = len(content)

        # Validates file size
        if size > self.MAX_FILE_SIZE_BYTES:
            self.logger.error(
                f"File size {size} exceeds maximum {self.MAX_FILE_SIZE_BYTES}"
            )
            return False

        if size == 0:
            self.logger.error(f"Empty file received")
            return False

        # Else return True
        return True
