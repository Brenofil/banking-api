"""
Interface for document conversion services.

This interface defines the contract for services that handle document conversion
using the Docling library or similar document processing tools.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import InputFormat


class DoclingServiceInterface(ABC):
    """
    Abstract interface for document conversion services.

    This interface defines all methods that a document conversion service should
    implement to support various document formats and processing requirements.
    It's designed to be extensible for future document types and processing needs.
    """

    @abstractmethod
    def configure_pdf_options(
        self, do_ocr: bool = True, do_table_structure: bool = True, **kwargs
    ) -> None:
        """
        Configure PDF-specific pipeline options.

        Args:
            do_ocr: Enable OCR for scanned documents (default: True)
            do_table_structure: Extract table structures (default: True)
            **kwargs: Additional PDF pipeline options
        """
        pass

    @abstractmethod
    def configure_docx_options(self, **kwargs) -> None:
        """
        Configure DOCX-specific pipeline options.

        Args:
            **kwargs: DOCX pipeline options (e.g., extract_images, preserve_formatting)
        """
        pass

    @abstractmethod
    def configure_xlsx_options(self, **kwargs) -> None:
        """
        Configure XLSX-specific pipeline options.

        Args:
            **kwargs: XLSX pipeline options (e.g., sheet_selection, formula_evaluation)
        """
        pass

    @abstractmethod
    def configure_csv_options(self, **kwargs) -> None:
        """
        Configure CSV-specific pipeline options.

        Args:
            **kwargs: CSV pipeline options (e.g., delimiter, encoding, header_detection)
        """
        pass

    @abstractmethod
    def set_format_options(self, format_options: Dict[InputFormat, Any]) -> None:
        """
        Set custom format options for multiple document types.

        This method allows setting options for multiple formats at once,
        useful for batch processing or multi-format support.

        Args:
            format_options: Dictionary mapping InputFormat to FormatOption
        """
        pass

    @abstractmethod
    def initialize_converter(self) -> None:
        """
        Initialize or reinitialize the document converter with current format options.

        This method should be called after configuring format options and before
        converting documents. It creates a new converter instance with the
        configured options.
        """
        pass

    @abstractmethod
    def get_converter(self) -> DocumentConverter:
        """
        Get the document converter, initializing it if necessary.

        Returns:
            DocumentConverter: The configured document converter

        Raises:
            RuntimeError: If converter initialization fails
        """
        pass


@abstractmethod
def convert_document(
    self,
    document_bytes: bytes,
    source_format: str = "pdf",
    password: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Convert document bytes into a structured format.

    Args:
        document_bytes: Raw document bytes to be converted
        source_format: Format of the source document (e.g., "pdf", "docx", "xlsx")
        password: Password for encrypted documents (optional, overrides configured password)

    Returns:
        Dict[str, Any]: Structured document data containing:
            - text: Extracted text content
            - tables: List of extracted tables
            - metadata: Document metadata
            - page_count: Number of pages (if applicable)
            - images: Information about images
            - sheets: List of sheets (for spreadsheets)
            - formulas: Extracted formulas (for spreadsheets)
            - is_encrypted: Whether document was encrypted

    Raises:
        ValueError: If document_bytes is empty or invalid, or if password is required but not provided
        RuntimeError: If conversion fails or password is incorrect
    """
    pass

    @abstractmethod
    def convert_document_async(
        self, document_bytes: bytes, source_format: str = "pdf"
    ) -> Any:
        """
        Asynchronously convert document bytes into a structured format.

        This method is for future implementation to support async processing
        of large documents without blocking.

        Args:
            document_bytes: Raw document bytes to be converted
            source_format: Format of the source document

        Returns:
            Awaitable[Dict[str, Any]]: Async result with structured document data

        Raises:
            ValueError: If document_bytes is empty or invalid
            RuntimeError: If conversion fails
        """
        pass

    @abstractmethod
    def validate_document(
        self, document_bytes: bytes, expected_format: Optional[str] = None
    ) -> bool:
        """
        Validate if document bytes can be processed.

        Args:
            document_bytes: Raw document bytes to validate
            expected_format: Expected format to validate against (optional)

        Returns:
            bool: True if document is valid, False otherwise
        """
        pass

    @abstractmethod
    def detect_format(self, document_bytes: bytes) -> Optional[str]:
        """
        Detect the format of a document from its bytes.

        This method analyzes the document bytes to determine the file format,
        useful when the format is unknown or needs verification.

        Args:
            document_bytes: Raw document bytes to analyze

        Returns:
            Optional[str]: Detected format (e.g., "pdf", "docx") or None if unknown
        """
        pass

    @abstractmethod
    def extract_metadata(
        self, document_bytes: bytes, source_format: str = "pdf"
    ) -> Optional[Dict[str, Any]]:
        """
        Extract only metadata from document without full processing.

        This is a lightweight operation for quick metadata extraction
        (e.g., author, creation date, page count) without processing the entire document.

        Args:
            document_bytes: Raw document bytes
            source_format: Format of the source document

        Returns:
            Optional[Dict[str, Any]]: Document metadata or None if not available
        """
        pass

    @abstractmethod
    def extract_text_only(
        self, document_bytes: bytes, source_format: str = "pdf"
    ) -> str:
        """
        Extract only text content from document without tables, images, etc.

        This is optimized for scenarios where only text content is needed,
        providing faster processing than full conversion.

        Args:
            document_bytes: Raw document bytes
            source_format: Format of the source document

        Returns:
            str: Extracted text content

        Raises:
            ValueError: If document_bytes is empty or invalid
            RuntimeError: If extraction fails
        """
        pass

    @abstractmethod
    def extract_tables(
        self, document_bytes: bytes, source_format: str = "pdf"
    ) -> List[Dict[str, Any]]:
        """
        Extract only tables from document.

        This is optimized for scenarios where only table data is needed,
        useful for data extraction and analysis tasks.

        Args:
            document_bytes: Raw document bytes
            source_format: Format of the source document

        Returns:
            List[Dict[str, Any]]: List of extracted tables with their data

        Raises:
            ValueError: If document_bytes is empty or invalid
            RuntimeError: If extraction fails
        """
        pass

    @abstractmethod
    def compare_documents(
        self, document1_bytes: bytes, document2_bytes: bytes, source_format: str = "pdf"
    ) -> Dict[str, Any]:
        """
        Compare two documents and return differences.

        This method is for future implementation to support document comparison,
        useful for version control and change tracking.

        Args:
            document1_bytes: First document bytes
            document2_bytes: Second document bytes
            source_format: Format of the documents

        Returns:
            Dict[str, Any]: Comparison results including:
                - differences: List of differences found
                - similarity_score: Similarity percentage
                - changed_sections: Sections that changed

        Raises:
            ValueError: If document bytes are invalid
            RuntimeError: If comparison fails
        """
        pass

    @abstractmethod
    def merge_documents(
        self, document_bytes_list: List[bytes], source_format: str = "pdf"
    ) -> bytes:
        """
        Merge multiple documents into a single document.

        This method is for future implementation to support document merging,
        useful for combining multiple files into one.

        Args:
            document_bytes_list: List of document bytes to merge
            source_format: Format of the documents

        Returns:
            bytes: Merged document bytes

        Raises:
            ValueError: If document list is empty or invalid
            RuntimeError: If merging fails
        """
        pass

    @abstractmethod
    def split_document(
        self,
        document_bytes: bytes,
        split_criteria: Dict[str, Any],
        source_format: str = "pdf",
    ) -> List[bytes]:
        """
        Split a document into multiple documents based on criteria.

        This method is for future implementation to support document splitting,
        useful for breaking large documents into smaller parts.

        Args:
            document_bytes: Document bytes to split
            split_criteria: Criteria for splitting (e.g., page_count, section_markers)
            source_format: Format of the document

        Returns:
            List[bytes]: List of split document bytes

        Raises:
            ValueError: If document bytes or criteria are invalid
            RuntimeError: If splitting fails
        """
        pass

    @abstractmethod
    def get_supported_formats(self) -> List[str]:
        """
        Get list of all supported document formats.

        Returns:
            List[str]: List of supported format identifiers (e.g., ["pdf", "docx", "xlsx"])
        """
        pass

    @abstractmethod
    def get_format_capabilities(self, format_type: str) -> Dict[str, bool]:
        """
        Get capabilities for a specific document format.

        Args:
            format_type: Format identifier (e.g., "pdf", "docx")

        Returns:
            Dict[str, bool]: Dictionary of capabilities:
                - ocr_support: Whether OCR is supported
                - table_extraction: Whether table extraction is supported
                - image_extraction: Whether image extraction is supported
                - metadata_extraction: Whether metadata extraction is supported
                - text_extraction: Whether text extraction is supported
        """
        pass

    @abstractmethod
    def clear_cache(self) -> None:
        """
        Clear any cached data or temporary files.

        This method should clean up resources used during document processing,
        useful for memory management in long-running applications.
        """
        pass

    @abstractmethod
    def get_processing_stats(self) -> Dict[str, Any]:
        """
        Get statistics about document processing.

        Returns:
            Dict[str, Any]: Processing statistics including:
                - total_documents_processed: Total number of documents processed
                - average_processing_time: Average processing time in milliseconds
                - success_rate: Percentage of successful conversions
                - format_breakdown: Number of documents processed per format
        """
        pass
