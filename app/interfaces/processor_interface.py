from abc import ABC, abstractmethod
from typing import List, Optional

from pydantic import Base64Bytes
from app.models.documents.processor import ProcessorResponse


class ProcessorInterface(ABC):
    """
    Abstract interface for document processors.

    Each processor implementation handles a specific document type (CSV, PDF, XLSX, etc.)
    using docling for document processing and extraction.
    """

    @abstractmethod
    def process(self, document_data: bytes) -> ProcessorResponse:
        """
        Process document data and extract structured information.

        Args:
            document_data: Raw document bytes to be processed

        Returns:
            ProcessorResponse: Structured response containing processing status and extracted data

        Raises:
            ValueError: If document_data is invalid or corrupted
            RuntimeError: If processing fails due to docling errors
        """
        pass

    @abstractmethod
    def validate(self, document_data: bytes) -> bool:
        """
        Validate if the document data is compatible with this processor.

        Args:
            document_data: Raw document bytes to validate

        Returns:
            bool: True if document can be processed by this processor, False otherwise
        """
        pass

    @abstractmethod
    def get_supported_extensions(self) -> List[str]:
        """
        Get list of file extensions supported by this processor.

        Returns:
            List[str]: List of supported file extensions (e.g., ['.pdf', '.PDF'])
        """
        pass

    @abstractmethod
    def get_supported_mime_types(self) -> List[str]:
        """
        Get list of MIME types supported by this processor.

        Returns:
            List[str]: List of supported MIME types (e.g., ['application/pdf'])
        """
        pass

    def preprocess(self, document_data: bytes) -> bytes:
        """
        Optional preprocessing step before main processing.

        Can be overridden by subclasses to perform document-specific preprocessing
        such as cleaning, normalization, or format conversion.

        Args:
            document_data: Raw document bytes

        Returns:
            bytes: Preprocessed document bytes
        """
        return document_data

    def postprocess(self, response: ProcessorResponse) -> ProcessorResponse:
        """
        Optional postprocessing step after main processing.

        Can be overridden by subclasses to perform additional data transformation,
        validation, or enrichment of the extracted data.

        Args:
            response: Initial processor response

        Returns:
            ProcessorResponse: Enhanced processor response
        """
        return response

    def get_metadata(self, document_data: bytes) -> Optional[dict]:
        """
        Extract metadata from document without full processing.

        Can be overridden by subclasses to provide quick metadata extraction
        (e.g., page count, author, creation date) without processing entire document.

        Args:
            document_data: Raw document bytes

        Returns:
            Optional[dict]: Document metadata or None if not available
        """
        return None
