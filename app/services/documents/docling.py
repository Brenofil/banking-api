import os
import re
from io import BytesIO
from typing import Dict, Any, Optional, List, Union
from pathlib import Path
import tempfile
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling_core.types.io import DocumentStream
from app.utils.logger import LoggerService
from app.interfaces.docling_service_interface import DoclingServiceInterface
from app.utils.markdown import MarkdownUtils


class DoclingService(DoclingServiceInterface):
    """
    Service responsible for all interaction with the docling extension.

    This service provides document conversion capabilities using the Docling library,
    converting various document formats into a structured, workable format.

    The service is designed to be flexible and support multiple document types
    through configurable format options and pipeline settings.

    Implements DoclingServiceInterface for standardized document processing operations.
    """

    name: str = "Docling Service"
    logger = LoggerService().get_logger(name)
    markdownUtils = MarkdownUtils()

    def __init__(self):
        """
        Initialize the Docling service with minimal configuration.

        The converter is initialized without format options, which can be
        configured later using set_format_options() or configure_pdf_options().

        Also sets up HuggingFace authentication if HF_TOKEN is available in environment.
        """
        self.logger.info("Initializing Docling Service")

        # Set up HuggingFace token for authenticated requests
        hf_token = os.getenv("HF_TOKEN")

        if hf_token:
            os.environ["HF_TOKEN"] = hf_token
            self.logger.info("HuggingFace token configured for authenticated requests")
        else:
            self.logger.warning(
                "HF_TOKEN not found in environment. "
                "Using unauthenticated requests to HuggingFace Hub. "
                "Set HF_TOKEN environment variable for higher rate limits and faster downloads. "
                "Get your token from: https://huggingface.co/settings/tokens"
            )

        # Initialize with no format options - will be configured per document type
        self.converter: Optional[DocumentConverter] = None
        self.format_options: Dict[InputFormat, Any] = {}

        self.logger.info("Docling Service initialized successfully")

    def configure_pdf_options(
        self,
        do_ocr: bool = True,
        do_table_structure: bool = True,
        password: Optional[str] = None,
        **kwargs,
    ) -> None:
        """
        Configure PDF-specific pipeline options.

        Args:
            do_ocr: Enable OCR for scanned documents (default: True)
            do_table_structure: Extract table structures (default: True)
            password: Password for encrypted PDFs (optional)
            **kwargs: Additional PDF pipeline options
        """
        self.logger.info("Configuring PDF pipeline options")

        pdf_options = PdfPipelineOptions()
        pdf_options.do_ocr = do_ocr
        pdf_options.do_table_structure = do_table_structure

        # Apply any additional options
        for key, value in kwargs.items():
            if hasattr(pdf_options, key):
                setattr(pdf_options, key, value)

        # Store password for later use if provided
        if password:
            self.pdf_password = password
            self.logger.info("PDF password configured for encrypted documents")
        else:
            self.pdf_password = None

        self.format_options[InputFormat.PDF] = PdfFormatOption(
            pipeline_options=pdf_options
        )

        self.logger.info(
            f"PDF options configured: OCR={do_ocr}, Tables={do_table_structure}, Password={'set' if password else 'not set'}"
        )

    def set_format_options(self, format_options: Dict[InputFormat, Any]) -> None:
        """
        Set custom format options for multiple document types.

        Args:
            format_options: Dictionary mapping InputFormat to FormatOption
        """
        self.logger.info(f"Setting format options for {len(format_options)} format(s)")
        self.format_options = format_options

    def initialize_converter(self) -> None:
        """
        Initialize or reinitialize the document converter with current format options.

        This method should be called after configuring format options and before
        converting documents.
        """
        self.logger.info("Initializing document converter")

        if self.format_options:
            self.converter = DocumentConverter(format_options=self.format_options)
            self.logger.info(
                f"Converter initialized with {len(self.format_options)} format option(s)"
            )
        else:
            self.converter = DocumentConverter()
            self.logger.info("Converter initialized with default options")

    def get_converter(self) -> DocumentConverter:
        """
        Get the document converter, initializing it if necessary.

        Returns:
            DocumentConverter: The configured document converter
        """
        if self.converter is None:
            self.initialize_converter()

        if self.converter is None:
            raise RuntimeError("Failed to initialize document converter")

        return self.converter

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
            source_format: Format of the source document (default: "pdf")
            password: Password for encrypted documents (optional, overrides configured password)

        Returns:
            Dict[str, Any]: Structured document data containing:
                - text: Extracted text content
                - tables: List of extracted tables
                - metadata: Document metadata
                - page_count: Number of pages
                - images: Information about images
                - is_encrypted: Whether document was encrypted

        Raises:
            ValueError: If document_bytes is empty or invalid, or if password is required but not provided
            RuntimeError: If conversion fails or password is incorrect
        """
        if not document_bytes:
            self.logger.error("Empty document bytes provided")
            raise ValueError("Document bytes cannot be empty")

        self.logger.info(f"Converting document of format: {source_format}")

        try:
            # Create a DocumentStream from bytes
            doc_stream = DocumentStream(
                name=f"document.{source_format}", stream=BytesIO(document_bytes)
            )

            # Get the converter (initializes if needed)
            converter = self.get_converter()

            # Convert the document
            result = converter.convert(doc_stream)

            # Extract structured data from the conversion result
            structured_data = self._extract_structured_data(result)

            self.logger.info("Document converted successfully")
            return structured_data

        except Exception as e:
            self.logger.error(f"Failed to convert document: {str(e)}")
            raise RuntimeError(f"Document conversion failed: {str(e)}")

    def _extract_structured_data(self, conversion_result) -> Dict[str, Any]:
        """
        Extract structured data from Docling conversion result.

        Args:
            conversion_result: Result object from Docling converter

        Returns:
            Dict[str, Any]: Structured data extracted from the document
        """
        try:
            # Get the document from the result
            doc = conversion_result.document

            # Extract text content
            extracted_text = (
                doc.export_to_markdown() if hasattr(doc, "export_to_markdown") else ""
            )

            # Extract tables from Docling's table detection
            tables = []
            if hasattr(doc, "tables") and doc.tables:
                for idx, table in enumerate(doc.tables):
                    try:
                        # Export table to dataframe (pass doc to avoid deprecation warning)
                        if hasattr(table, "export_to_dataframe"):
                            df = table.export_to_dataframe(doc)
                            table_dict = df.to_dict()
                            rows = len(df)
                            columns = len(df.columns) if len(df) > 0 else 0
                        else:
                            table_dict = {}
                            rows = 0
                            columns = 0

                        table_data = {
                            "index": idx,
                            "data": table_dict,
                            "rows": rows,
                            "columns": columns,
                            "source": "docling_detection",
                        }
                        tables.append(table_data)
                    except Exception as e:
                        # Log the error but continue processing other tables
                        self.logger.warning(f"Failed to extract table {idx}: {str(e)}")
                        continue

            # Also extract markdown tables from the text
            markdown_tables = self.markdownUtils._parse_markdown_tables(extracted_text)

            # Deduplicate: only add markdown tables that aren't similar to existing ones
            for md_table in markdown_tables:
                if not self._is_duplicate_table(md_table, tables):
                    tables.append(
                        {
                            "index": len(tables),
                            "data": md_table["data"],
                            "rows": md_table["rows"],
                            "columns": md_table["columns"],
                            "source": "markdown_parsing",
                        }
                    )
                else:
                    self.logger.debug(
                        f"Skipping duplicate markdown table with {md_table['rows']} rows and {md_table['columns']} columns"
                    )

            # Extract metadata
            metadata = {}
            if hasattr(doc, "metadata"):
                metadata = {
                    "title": getattr(doc.metadata, "title", None),
                    "author": getattr(doc.metadata, "author", None),
                    "creation_date": getattr(doc.metadata, "creation_date", None),
                    "modification_date": getattr(
                        doc.metadata, "modification_date", None
                    ),
                }

            # Extract page count
            page_count = len(doc.pages) if hasattr(doc, "pages") else 0

            # Extract images information
            images = []
            if hasattr(doc, "pictures") and doc.pictures:
                for idx, picture in enumerate(doc.pictures):
                    image_info = {
                        "index": idx,
                        "page": getattr(picture, "page", None),
                        "format": getattr(picture, "format", None),
                        "width": getattr(picture, "width", None),
                        "height": getattr(picture, "height", None),
                    }
                    images.append(image_info)

            return {
                "text": extracted_text,
                "tables": tables,
                "metadata": metadata,
                "page_count": page_count,
                "images": images,
            }

        except Exception as e:
            self.logger.error(f"Failed to extract structured data: {str(e)}")
            raise RuntimeError(f"Data extraction failed: {str(e)}")

    def _is_duplicate_table(
        self, new_table: Dict[str, Any], existing_tables: List[Dict[str, Any]]
    ) -> bool:
        """
        Check if a table is a duplicate of any existing table.

        A table is considered duplicate if it has the same dimensions (rows/columns)
        and similar content (>80% matching cells).

        Args:
            new_table: New table to check
            existing_tables: List of existing tables

        Returns:
            bool: True if table is a duplicate, False otherwise
        """
        new_rows = new_table.get("rows", 0)
        new_cols = new_table.get("columns", 0)
        new_data = new_table.get("data", {})

        for existing in existing_tables:
            existing_rows = existing.get("rows", 0)
            existing_cols = existing.get("columns", 0)

            # Check if dimensions match
            if new_rows != existing_rows or new_cols != existing_cols:
                continue

            # Check content similarity
            existing_data = existing.get("data", {})

            # Count matching cells
            total_cells = 0
            matching_cells = 0

            for col_key in new_data.keys():
                if col_key in existing_data:
                    new_col = new_data[col_key]
                    existing_col = existing_data[col_key]

                    for row_key in new_col.keys():
                        total_cells += 1
                        if row_key in existing_col:
                            # Compare cell values (strip whitespace for comparison)
                            new_val = str(new_col[row_key]).strip()
                            existing_val = str(existing_col[row_key]).strip()
                            if new_val == existing_val:
                                matching_cells += 1

            # If >80% of cells match, consider it a duplicate
            if total_cells > 0 and (matching_cells / total_cells) > 0.8:
                return True

        return False

    def configure_docx_options(self, **kwargs) -> None:
        """
        Configure DOCX-specific pipeline options.

        Args:
            **kwargs: DOCX pipeline options
        """
        self.logger.info("DOCX options configuration not yet implemented")
        # TODO: Implement DOCX configuration when DOCX processor is added
        pass

    def configure_xlsx_options(self, **kwargs) -> None:
        """
        Configure XLSX-specific pipeline options.

        Args:
            **kwargs: XLSX pipeline options
        """
        self.logger.info("XLSX options configuration not yet implemented")
        # TODO: Implement XLSX configuration when XLSX processor is added
        pass

    def configure_csv_options(self, **kwargs) -> None:
        """
        Configure CSV-specific pipeline options.

        Args:
            **kwargs: CSV pipeline options
        """
        self.logger.info("CSV options configuration not yet implemented")
        # TODO: Implement CSV configuration when CSV processor is added
        pass

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
        if not document_bytes or len(document_bytes) == 0:
            self.logger.warning("Document validation failed: empty bytes")
            return False

        # Check if bytes start with PDF signature
        if document_bytes[:4] == b"%PDF":
            if expected_format and expected_format.lower() != "pdf":
                self.logger.warning(f"Document is PDF but expected {expected_format}")
                return False
            self.logger.info("Document validated as PDF")
            return True

        self.logger.warning("Document validation failed: unknown format")
        return False

    def detect_format(self, document_bytes: bytes) -> Optional[str]:
        """
        Detect the format of a document from its bytes.

        Args:
            document_bytes: Raw document bytes to analyze

        Returns:
            Optional[str]: Detected format or None if unknown
        """
        if not document_bytes or len(document_bytes) < 4:
            return None

        # Check PDF signature
        if document_bytes[:4] == b"%PDF":
            return "pdf"

        # Check ZIP-based formats (DOCX, XLSX)
        if document_bytes[:4] == b"PK\x03\x04":
            # Could be DOCX, XLSX, or other ZIP-based format
            # More sophisticated detection would be needed
            return "zip-based"

        return None

    def extract_metadata(
        self, document_bytes: bytes, source_format: str = "pdf"
    ) -> Optional[Dict[str, Any]]:
        """
        Extract only metadata from document without full processing.

        Args:
            document_bytes: Raw document bytes
            source_format: Format of the source document

        Returns:
            Optional[Dict[str, Any]]: Document metadata or None
        """
        self.logger.info("Metadata-only extraction not yet implemented")
        # TODO: Implement lightweight metadata extraction
        return None

    def extract_text_only(
        self, document_bytes: bytes, source_format: str = "pdf"
    ) -> str:
        """
        Extract only text content from document.

        Args:
            document_bytes: Raw document bytes
            source_format: Format of the source document

        Returns:
            str: Extracted text content
        """
        self.logger.info("Text-only extraction - using full conversion")
        result = self.convert_document(document_bytes, source_format)
        return result.get("text", "")

    def extract_tables(
        self, document_bytes: bytes, source_format: str = "pdf"
    ) -> List[Dict[str, Any]]:
        """
        Extract only tables from document.

        Args:
            document_bytes: Raw document bytes
            source_format: Format of the source document

        Returns:
            List[Dict[str, Any]]: List of extracted tables
        """
        self.logger.info("Table-only extraction - using full conversion")
        result = self.convert_document(document_bytes, source_format)
        return result.get("tables", [])

    def convert_document_async(
        self, document_bytes: bytes, source_format: str = "pdf"
    ) -> Any:
        """
        Asynchronously convert document bytes (not yet implemented).

        Args:
            document_bytes: Raw document bytes
            source_format: Format of the source document

        Returns:
            Awaitable result
        """
        raise NotImplementedError("Async conversion not yet implemented")

    def compare_documents(
        self, document1_bytes: bytes, document2_bytes: bytes, source_format: str = "pdf"
    ) -> Dict[str, Any]:
        """
        Compare two documents (not yet implemented).

        Args:
            document1_bytes: First document bytes
            document2_bytes: Second document bytes
            source_format: Format of the documents

        Returns:
            Dict[str, Any]: Comparison results
        """
        raise NotImplementedError("Document comparison not yet implemented")

    def merge_documents(
        self, document_bytes_list: List[bytes], source_format: str = "pdf"
    ) -> bytes:
        """
        Merge multiple documents (not yet implemented).

        Args:
            document_bytes_list: List of document bytes to merge
            source_format: Format of the documents

        Returns:
            bytes: Merged document bytes
        """
        raise NotImplementedError("Document merging not yet implemented")

    def split_document(
        self,
        document_bytes: bytes,
        split_criteria: Dict[str, Any],
        source_format: str = "pdf",
    ) -> List[bytes]:
        """
        Split a document (not yet implemented).

        Args:
            document_bytes: Document bytes to split
            split_criteria: Criteria for splitting
            source_format: Format of the document

        Returns:
            List[bytes]: List of split document bytes
        """
        raise NotImplementedError("Document splitting not yet implemented")

    def get_supported_formats(self) -> List[str]:
        """
        Get list of all supported document formats.

        Returns:
            List[str]: List of supported formats
        """
        return ["pdf"]  # Currently only PDF is fully supported

    def get_format_capabilities(self, format_type: str) -> Dict[str, bool]:
        """
        Get capabilities for a specific document format.

        Args:
            format_type: Format identifier

        Returns:
            Dict[str, bool]: Dictionary of capabilities
        """
        if format_type.lower() == "pdf":
            return {
                "ocr_support": True,
                "table_extraction": True,
                "image_extraction": True,
                "metadata_extraction": True,
                "text_extraction": True,
            }
        return {
            "ocr_support": False,
            "table_extraction": False,
            "image_extraction": False,
            "metadata_extraction": False,
            "text_extraction": False,
        }

    def clear_cache(self) -> None:
        """
        Clear any cached data or temporary files.
        """
        self.logger.info("Cache clearing not yet implemented")
        # TODO: Implement cache management
        pass

    def get_processing_stats(self) -> Dict[str, Any]:
        """
        Get statistics about document processing.

        Returns:
            Dict[str, Any]: Processing statistics
        """
        self.logger.info("Processing stats not yet implemented")
        # TODO: Implement statistics tracking
        return {
            "total_documents_processed": 0,
            "average_processing_time": 0.0,
            "success_rate": 0.0,
            "format_breakdown": {},
        }
