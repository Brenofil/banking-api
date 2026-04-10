"""File extension enum for document processors."""

from enum import Enum


class FileExtension(str, Enum):
    """
    Supported file extensions for document processing.

    This enum defines all file extensions that can be processed by the application's
    document processors. Each extension maps to a specific processor implementation.

    Attributes:
        PDF: Portable Document Format files (.pdf)
        CSV: Comma-Separated Values files (.csv)
        XLSX: Microsoft Excel Open XML Spreadsheet files (.xlsx)
        XLS: Microsoft Excel Binary File Format files (.xls)
        DOCX: Microsoft Word Open XML Document files (.docx)
        DOC: Microsoft Word Binary File Format files (.doc)
        TXT: Plain text files (.txt)
        JSON: JavaScript Object Notation files (.json)
        XML: Extensible Markup Language files (.xml)

    Usage:
        from app.enums.file_extensions import FileExtension

        # Check if extension is supported
        extension = ".pdf"
        if extension in [e.value for e in FileExtension]:
            print(f"{extension} is supported")

        # Get extension enum
        ext_enum = FileExtension.PDF
        print(ext_enum.value)  # ".pdf"
    """

    PDF = ".pdf"
    CSV = ".csv"
    XLSX = ".xlsx"
    XLS = ".xls"
    DOCX = ".docx"
    DOC = ".doc"
    TXT = ".txt"
    JSON = ".json"
    XML = ".xml"

    def get_file_type(self) -> str:
        """
        Get the file type identifier for this extension.

        Returns:
            str: File type identifier (e.g., 'pdf', 'csv', 'xlsx')

        Example:
            >>> FileExtension.PDF.get_file_type()
            'pdf'
            >>> FileExtension.XLSX.get_file_type()
            'xlsx'
        """
        # Map extension enum to file type
        extension_to_type = {
            self.PDF: "pdf",
            self.CSV: "csv",
            self.XLSX: "xlsx",
            self.XLS: "xls",
            self.DOCX: "docx",
            self.DOC: "doc",
            self.TXT: "txt",
            self.JSON: "json",
            self.XML: "xml",
        }
        return extension_to_type[self]

    @classmethod
    def get_extension_to_type_map(cls) -> dict[str, str]:
        """
        Get mapping of file extensions to file type identifiers.

        Returns:
            dict[str, str]: Dictionary mapping extensions to file types

        Example:
            >>> FileExtension.get_extension_to_type_map()
            {'.pdf': 'pdf', '.csv': 'csv', '.xlsx': 'xlsx', ...}
        """
        return {ext.value: ext.get_file_type() for ext in cls}

    @classmethod
    def from_file_type(cls, file_type: str) -> "FileExtension":
        """
        Get the primary extension for a given file type.

        Args:
            file_type: File type identifier (e.g., 'pdf', 'csv')

        Returns:
            FileExtension: Primary extension for the file type

        Raises:
            ValueError: If file type is not recognized

        Example:
            >>> FileExtension.from_file_type('pdf')
            <FileExtension.PDF: '.pdf'>
        """
        type_to_extension = {
            "pdf": cls.PDF,
            "csv": cls.CSV,
            "xlsx": cls.XLSX,
            "xls": cls.XLS,
            "docx": cls.DOCX,
            "doc": cls.DOC,
            "txt": cls.TXT,
            "json": cls.JSON,
            "xml": cls.XML,
        }

        file_type_lower = file_type.lower().strip()
        if file_type_lower not in type_to_extension:
            raise ValueError(
                f"Unknown file type: {file_type}. "
                f"Known types: {', '.join(type_to_extension.keys())}"
            )

        return type_to_extension[file_type_lower]

    @classmethod
    def from_string(cls, extension: str) -> "FileExtension":
        """
        Convert a string to FileExtension enum, handling with or without leading dot.

        Args:
            extension: File extension string (e.g., "pdf", ".pdf", "PDF", ".PDF")

        Returns:
            FileExtension: Corresponding enum value

        Raises:
            ValueError: If extension is not supported

        Example:
            >>> FileExtension.from_string("pdf")
            <FileExtension.PDF: '.pdf'>
            >>> FileExtension.from_string(".PDF")
            <FileExtension.PDF: '.pdf'>
        """
        # Normalize: lowercase and ensure leading dot
        normalized = extension.lower()
        if not normalized.startswith("."):
            normalized = f".{normalized}"

        try:
            return cls(normalized)
        except ValueError:
            raise ValueError(
                f"Unsupported file extension: {extension}. "
                f"Supported extensions: {', '.join([e.value for e in cls])}"
            )

    @classmethod
    def get_all_extensions(cls) -> list[str]:
        """
        Get list of all supported file extensions.

        Returns:
            list[str]: List of all extension values

        Example:
            >>> FileExtension.get_all_extensions()
            ['.pdf', '.csv', '.xlsx', '.xls', '.docx', '.doc', '.txt', '.json', '.xml']
        """
        return [e.value for e in cls]

    @classmethod
    def is_supported(cls, extension: str) -> bool:
        """
        Check if a file extension is supported.

        Args:
            extension: File extension to check (with or without leading dot)

        Returns:
            bool: True if extension is supported, False otherwise

        Example:
            >>> FileExtension.is_supported(".pdf")
            True
            >>> FileExtension.is_supported("txt")
            True
            >>> FileExtension.is_supported(".xyz")
            False
        """
        try:
            cls.from_string(extension)
            return True
        except ValueError:
            return False
