"""MIME type enum for document processors."""

from enum import Enum


class MimeType(str, Enum):
    """
    Supported MIME types for document processing.

    This enum defines all MIME types that can be processed by the application's
    document processors. Each MIME type maps to a specific processor implementation.

    MIME types follow the standard format: type/subtype
    Reference: https://www.iana.org/assignments/media-types/media-types.xhtml

    Attributes:
        PDF: Portable Document Format (application/pdf)
        CSV: Comma-Separated Values (text/csv)
        XLSX: Microsoft Excel Open XML Spreadsheet (application/vnd.openxmlformats-officedocument.spreadsheetml.sheet)
        XLS: Microsoft Excel Binary File Format (application/vnd.ms-excel)
        DOCX: Microsoft Word Open XML Document (application/vnd.openxmlformats-officedocument.wordprocessingml.document)
        DOC: Microsoft Word Binary File Format (application/msword)
        TXT: Plain text (text/plain)
        JSON: JavaScript Object Notation (application/json)
        XML: Extensible Markup Language (application/xml or text/xml)

    Usage:
        from app.enums.mime_types import MimeType

        # Check if MIME type is supported
        mime = "application/pdf"
        if mime in [m.value for m in MimeType]:
            print(f"{mime} is supported")

        # Get MIME type enum
        mime_enum = MimeType.PDF
        print(mime_enum.value)  # "application/pdf"
    """

    PDF = "application/pdf"
    CSV = "text/csv"
    XLSX = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    XLS = "application/vnd.ms-excel"
    DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    DOC = "application/msword"
    TXT = "text/plain"
    JSON = "application/json"
    XML = "application/xml"
    XML_TEXT = "text/xml"

    @classmethod
    def from_string(cls, mime_type: str) -> "MimeType":
        """
        Convert a string to MimeType enum.

        Args:
            mime_type: MIME type string (e.g., "application/pdf", "text/csv")

        Returns:
            MimeType: Corresponding enum value

        Raises:
            ValueError: If MIME type is not supported

        Example:
            >>> MimeType.from_string("application/pdf")
            <MimeType.PDF: 'application/pdf'>
            >>> MimeType.from_string("text/csv")
            <MimeType.CSV: 'text/csv'>
        """
        # Normalize: lowercase and strip whitespace
        normalized = mime_type.lower().strip()

        # Handle special case for XML (both application/xml and text/xml)
        if normalized in ("application/xml", "text/xml"):
            return cls.XML if normalized == "application/xml" else cls.XML_TEXT

        try:
            return cls(normalized)
        except ValueError:
            raise ValueError(
                f"Unsupported MIME type: {mime_type}. "
                f"Supported types: {', '.join([m.value for m in cls])}"
            )

    @classmethod
    def get_all_mime_types(cls) -> list[str]:
        """
        Get list of all supported MIME types.

        Returns:
            list[str]: List of all MIME type values

        Example:
            >>> MimeType.get_all_mime_types()
            ['application/pdf', 'text/csv', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', ...]
        """
        return [m.value for m in cls]

    @classmethod
    def is_supported(cls, mime_type: str) -> bool:
        """
        Check if a MIME type is supported.

        Args:
            mime_type: MIME type to check

        Returns:
            bool: True if MIME type is supported, False otherwise

        Example:
            >>> MimeType.is_supported("application/pdf")
            True
            >>> MimeType.is_supported("text/csv")
            True
            >>> MimeType.is_supported("application/unknown")
            False
        """
        try:
            cls.from_string(mime_type)
            return True
        except ValueError:
            return False

    @classmethod
    def get_mime_type_for_extension(cls, extension: str) -> "MimeType":
        """
        Get the MIME type for a given file extension.

        Args:
            extension: File extension (with or without leading dot)

        Returns:
            MimeType: Corresponding MIME type enum

        Raises:
            ValueError: If extension is not supported

        Example:
            >>> MimeType.get_mime_type_for_extension(".pdf")
            <MimeType.PDF: 'application/pdf'>
            >>> MimeType.get_mime_type_for_extension("csv")
            <MimeType.CSV: 'text/csv'>
        """
        # Normalize extension
        ext = extension.lower().strip()
        if not ext.startswith("."):
            ext = f".{ext}"

        # Map extensions to MIME types
        extension_map = {
            ".pdf": cls.PDF,
            ".csv": cls.CSV,
            ".xlsx": cls.XLSX,
            ".xls": cls.XLS,
            ".docx": cls.DOCX,
            ".doc": cls.DOC,
            ".txt": cls.TXT,
            ".json": cls.JSON,
            ".xml": cls.XML,
        }

        if ext not in extension_map:
            raise ValueError(
                f"No MIME type mapping for extension: {extension}. "
                f"Supported extensions: {', '.join(extension_map.keys())}"
            )

        return extension_map[ext]
