"""Processing status enum for document processors."""

from enum import Enum


class ProcessingStatus(str, Enum):
    """
    Status codes for document processing operations.

    Attributes:
        SUCCESS: Document processed successfully with all data extracted
        PARTIAL_SUCCESS: Document processed but with some issues or incomplete data
        FAILED: Document processing failed completely
        VALIDATION_ERROR: Document failed validation checks
        UNSUPPORTED_FORMAT: Document format is not supported by the processor
    """

    SUCCESS = "success"
    PARTIAL_SUCCESS = "partial_success"
    FAILED = "failed"
    VALIDATION_ERROR = "validation_error"
    UNSUPPORTED_FORMAT = "unsupported_format"
