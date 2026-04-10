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
