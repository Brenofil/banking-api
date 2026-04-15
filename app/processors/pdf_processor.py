import time
from io import BytesIO
from typing_extensions import Any, List, Optional
from app.interfaces.processor_interface import ProcessorInterface
from app.models.documents.processor import ProcessorResponse
from app.utils import markdown
from app.utils.logger import LoggerService
from app.services.docling import DoclingService
from app.enums.processing_status import ProcessingStatus
from app.enums.file_extensions import FileExtension
from app.enums.mime_types import MimeType

try:
    import pikepdf

    PIKEPDF_AVAILABLE = True
except ImportError:
    pikepdf = None  # type: ignore
    PIKEPDF_AVAILABLE = False


class PdfDocumentProcessor(ProcessorInterface):
    """
    Document processor responsible for all the PDF document
    data processing. This class implements the ProcessorInterface
    and uses DoclingService for document conversion.
    """

    name: str = "PDF document processor"
    logger = LoggerService().get_logger(name)
    markdownUtils = markdown.MarkdownUtils()

    def __init__(self):
        """Initialize the PDF processor with DoclingService."""
        self.docling_service = DoclingService()
        self.current_password: Optional[str] = None  # Store password for preprocessing

        # Configure PDF-specific options (without password - will be handled in preprocess)
        self.docling_service.configure_pdf_options(do_ocr=True, do_table_structure=True)

        # Initialize the converter with configured options
        self.docling_service.initialize_converter()

        if not PIKEPDF_AVAILABLE:
            self.logger.warning(
                "pikepdf not available - password-protected PDFs cannot be decrypted"
            )

        self.logger.info(f"{self.name} initialized with DoclingService")

    def getName(self) -> str:
        """Get the processor name."""
        return self.name

    def process(
        self, content: bytes, password: Optional[str] = None
    ) -> ProcessorResponse:
        """
        Process PDF document content using DoclingService.

        Args:
            content: Raw PDF document bytes
            password: Optional password for encrypted PDFs

        Returns:
            ProcessorResponse: Structured response with extracted data
        """
        self.logger.info("Processing PDF document content")

        start_time: float = time.time()
        errors: list[Any] = []
        warnings: list[Any] = []

        try:
            # Store password for preprocessing
            self.current_password = password

            # Preprocess the content (handles decryption if needed)
            preprocessed_content = self.preprocess(content)

            # Validate the document first
            if not self.validate(preprocessed_content):
                self.logger.error("Document validation failed")

                # Check if it's an unsupported format
                detected_format = self.docling_service.detect_format(
                    preprocessed_content
                )

                if detected_format and detected_format != "pdf":
                    return ProcessorResponse(
                        status=ProcessingStatus.UNSUPPORTED_FORMAT,
                        processor_type="pdf",
                        errors=[
                            f"Unsupported format detected: {detected_format}. Expected PDF format."
                        ],
                        processing_time_ms=(time.time() - start_time) * 1000,
                    )

                return ProcessorResponse(
                    status=ProcessingStatus.VALIDATION_ERROR,
                    processor_type="pdf",
                    errors=[
                        "Document validation failed - invalid or corrupted PDF format"
                    ],
                    processing_time_ms=(time.time() - start_time) * 1000,
                )

            # Convert document using DoclingService (no password needed - already decrypted)
            self.logger.info("Converting document with DoclingService")
            structured_data = self.docling_service.convert_document(
                document_bytes=preprocessed_content,
                source_format="pdf",
            )

            # Check for partial success indicators
            page_count = structured_data.get("page_count", 0)
            extracted_text = structured_data.get("text", "")
            tables = structured_data.get("tables", [])
            images = structured_data.get("images", [])

            # Determine if processing was partial
            if page_count == 0:
                warnings.append("Could not determine page count")

            if not extracted_text or len(extracted_text.strip()) == 0:
                warnings.append(
                    "No text content extracted - document may be image-based or empty"
                )

            # Check if we got minimal data
            has_minimal_data = bool(extracted_text or tables or images)

            if not has_minimal_data:
                errors.append("Failed to extract any meaningful content from document")
                return ProcessorResponse(
                    status=ProcessingStatus.FAILED,
                    processor_type="pdf",
                    errors=errors,
                    warnings=warnings,
                    processing_time_ms=(time.time() - start_time) * 1000,
                )

            # Determine final status
            if warnings or (page_count > 0 and len(extracted_text.strip()) < 50):
                # Partial success if we have warnings or very little text
                status = ProcessingStatus.PARTIAL_SUCCESS
                if not warnings:
                    warnings.append(
                        "Extracted content is minimal - document may have processing issues"
                    )
            else:
                status = ProcessingStatus.SUCCESS

            # Calculate confidence score based on extraction quality
            confidence_score = self._calculate_confidence_score(
                extracted_text, tables, images, page_count, warnings
            )

            # Build the processor response
            response = ProcessorResponse(
                status=status,
                data=structured_data,
                metadata=structured_data.get("metadata"),
                processor_type="pdf",
                processing_time_ms=(time.time() - start_time) * 1000,
                extracted_text=extracted_text,
                page_count=page_count,
                tables=tables,
                images=images,
                errors=errors if errors else None,
                warnings=warnings if warnings else None,
                confidence_score=confidence_score,
            )

            # Postprocess the response if needed
            final_response = self.postprocess(response)

            self.logger.info(
                f"PDF document processed with status {status} in {final_response.processing_time_ms:.2f}ms "
                f"(confidence: {confidence_score:.2f})"
            )
            return final_response

        except ValueError as e:
            self.logger.error(f"Validation error during processing: {str(e)}")
            return ProcessorResponse(
                status=ProcessingStatus.VALIDATION_ERROR,
                processor_type="pdf",
                errors=[str(e)],
                processing_time_ms=(time.time() - start_time) * 1000,
            )
        except RuntimeError as e:
            self.logger.error(f"Runtime error during processing: {str(e)}")
            return ProcessorResponse(
                status=ProcessingStatus.FAILED,
                processor_type="pdf",
                errors=[str(e)],
                processing_time_ms=(time.time() - start_time) * 1000,
            )
        except Exception as e:
            self.logger.error(f"Unexpected error during processing: {str(e)}")
            return ProcessorResponse(
                status=ProcessingStatus.FAILED,
                processor_type="pdf",
                errors=[f"Unexpected error: {str(e)}"],
                processing_time_ms=(time.time() - start_time) * 1000,
            )

    def validate(self, document_data: bytes) -> bool:
        """
        Validate if the document data is a valid PDF.

        Args:
            document_data: Raw document bytes to validate

        Returns:
            bool: True if document is valid PDF, False otherwise
        """
        self.logger.info("Validating PDF document")

        if not document_data or len(document_data) == 0:
            self.logger.warning("Document validation failed: empty bytes")
            return False

        # Use DoclingService validation
        is_valid = self.docling_service.validate_document(document_data)

        if is_valid:
            self.logger.info("PDF document validated successfully")
        else:
            self.logger.warning("PDF document validation failed")

        return is_valid

    def _calculate_confidence_score(
        self,
        extracted_text: str,
        tables: List,
        images: List,
        page_count: int,
        warnings: List[str],
    ) -> float:
        """
        Calculate confidence score based on extraction quality.

        Args:
            extracted_text: Extracted text content
            tables: List of extracted tables
            images: List of extracted images
            page_count: Number of pages
            warnings: List of warnings

        Returns:
            float: Confidence score between 0.0 and 1.0
        """
        score = 1.0

        # Reduce score for warnings
        if warnings:
            score -= 0.1 * len(warnings)

        # Reduce score if no text extracted
        if not extracted_text or len(extracted_text.strip()) == 0:
            score -= 0.3
        elif len(extracted_text.strip()) < 50:
            score -= 0.2

        # Reduce score if page count is unknown
        if page_count == 0:
            score -= 0.1

        # Increase score if tables were extracted
        if tables and len(tables) > 0:
            score += 0.05

        # Increase score if images were detected
        if images and len(images) > 0:
            score += 0.05

        # Ensure score is between 0.0 and 1.0
        return max(0.0, min(1.0, score))

    def get_supported_extensions(self) -> List[str]:
        """
        Get list of supported file extensions.

        Returns:
            List[str]: List of supported extensions
        """
        return [FileExtension.PDF.value]

    def get_supported_mime_types(self) -> List[str]:
        """
        Get list of supported MIME types.

        Returns:
            List[str]: List of supported MIME types
        """
        return [MimeType.PDF.value]

    def preprocess(self, content: bytes) -> bytes:
        """
        Preprocess PDF content, handling decryption if needed.

        This method checks if the PDF is encrypted and attempts to decrypt it
        using the password stored in self.current_password (set by process()).

        Args:
            content: Raw document bytes

        Returns:
            bytes: Preprocessed (potentially decrypted) document bytes

        Raises:
            RuntimeError: If PDF is encrypted but no password provided or wrong password
            RuntimeError: If pikepdf is not available for encrypted PDFs
        """
        self.logger.debug("Preprocessing PDF content")

        # Check if PDF is encrypted
        is_encrypted = self._is_pdf_encrypted(content)

        if not is_encrypted:
            self.logger.debug("PDF is not encrypted, no preprocessing needed")
            return content

        self.logger.info("PDF is encrypted, attempting decryption")

        # Check if pikepdf is available
        if not PIKEPDF_AVAILABLE:
            raise RuntimeError(
                "PDF is encrypted but pikepdf is not installed. "
                "Install it with: pip install pikepdf"
            )

        # Check if password was provided
        if not self.current_password:
            raise RuntimeError(
                "PDF is encrypted but no password was provided. "
                "Please provide a password to decrypt the document."
            )

        try:
            # Decrypt the PDF using pikepdf
            if pikepdf is None:
                raise RuntimeError("pikepdf module is not available")

            pdf = pikepdf.open(BytesIO(content), password=self.current_password)
            decrypted_stream = BytesIO()
            pdf.save(decrypted_stream)
            decrypted_bytes = decrypted_stream.getvalue()

            self.logger.info("PDF decrypted successfully")
            return decrypted_bytes

        except Exception as e:
            # Check if it's a password error
            if (
                pikepdf
                and hasattr(pikepdf, "PasswordError")
                and isinstance(e, pikepdf.PasswordError)
            ):
                raise RuntimeError("Failed to decrypt PDF: incorrect password provided")
            raise RuntimeError(f"Failed to decrypt PDF: {str(e)}")

    def _is_pdf_encrypted(self, content: bytes) -> bool:
        """
        Check if a PDF is encrypted.

        Args:
            content: Raw PDF bytes

        Returns:
            bool: True if PDF is encrypted, False otherwise
        """
        if not PIKEPDF_AVAILABLE:
            # If pikepdf is not available, we can't check encryption status
            # Return False to avoid blocking non-encrypted PDFs
            return False

        try:
            # Try to open without password - if it fails, it's encrypted
            if pikepdf is None:
                return False

            pdf = pikepdf.open(BytesIO(content))
            pdf.close()
            return False
        except Exception as e:
            # Check if it's a password error (means encrypted)
            if pikepdf and isinstance(e, pikepdf.PasswordError):
                return True
            # If we can't determine, assume not encrypted
            return False

    def postprocess(self, response: ProcessorResponse) -> ProcessorResponse:
        """
        Postprocessing step to convert tables to DataFrames.

        Args:
            response: Initial processor response

        Returns:
            ProcessorResponse: Enhanced processor response with dataframes field
        """
        self.logger.info(f"Postprocessing response for {self.name}")

        # Only process if we have data and tables
        if not response.data or not response.tables:
            self.logger.debug("No tables to convert to DataFrames")
            return response

        try:
            # Convert tables to DataFrames
            dataframes = self.markdownUtils.read_pdf_response_to_dataframes(
                response.data
            )

            # Convert DataFrames to serializable format (dict)
            if isinstance(dataframes, list):
                # Multiple DataFrames - convert each to dict
                serializable_dfs = [
                    {
                        "data": df.to_dict(orient="records"),
                        "columns": df.columns.tolist(),
                        "shape": df.shape,
                        "index": list(range(len(df))),
                    }
                    for df in dataframes
                ]
                if response.data:
                    response.data["dataframes"] = serializable_dfs
                    self.logger.info(
                        f"Successfully added {len(serializable_dfs)} DataFrames to response"
                    )
            else:
                # Single DataFrame - convert to dict
                serializable_df = {
                    "data": dataframes.to_dict(orient="records"),
                    "columns": dataframes.columns.tolist(),
                    "shape": dataframes.shape,
                    "index": list(range(len(dataframes))),
                }
                if response.data:
                    response.data["dataframes"] = serializable_df
                    self.logger.info("Successfully added single DataFrame to response")

        except Exception as e:
            self.logger.warning(f"Failed to convert tables to DataFrames: {str(e)}")
            # Don't fail the entire response, just log the warning

        return response

    def get_metadata(self, document_data: bytes) -> Optional[dict]:
        """
        Extract metadata from PDF document without full processing.

        Args:
            document_data: Raw document bytes

        Returns:
            Optional[dict]: Document metadata or None if not available
        """
        self.logger.info("Extracting metadata from PDF document")

        try:
            # For quick metadata extraction, we could use a lightweight approach
            # For now, we'll return None and rely on full processing
            # In the future, this could be optimized to extract only metadata
            return None
        except Exception as e:
            self.logger.error(f"Failed to extract metadata: {str(e)}")
            return None
