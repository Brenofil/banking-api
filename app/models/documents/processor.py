from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.enums.processing_status import ProcessingStatus


class ProcessorResponse(BaseModel):
    """
    Comprehensive response model for document processor operations.

    Contains processing status, extracted data, metadata, and error information
    to provide complete feedback on document processing results.
    """

    status: ProcessingStatus = Field(
        ..., description="Processing status indicating success or failure type"
    )

    data: Optional[Dict[str, Any]] = Field(
        default=None, description="Extracted structured data from the document"
    )

    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Document metadata (e.g., page count, author, creation date, file size)",
    )

    processor_type: str = Field(
        ..., description="Type of processor used (e.g., 'pdf', 'csv', 'xlsx')"
    )

    processing_time_ms: Optional[float] = Field(
        default=None, description="Time taken to process the document in milliseconds"
    )

    errors: Optional[List[str]] = Field(
        default=None,
        description="List of error messages if processing failed or partially succeeded",
    )

    warnings: Optional[List[str]] = Field(
        default=None, description="List of warning messages for non-critical issues"
    )

    extracted_text: Optional[str] = Field(
        default=None, description="Raw text extracted from the document"
    )

    page_count: Optional[int] = Field(
        default=None, description="Number of pages in the document (if applicable)"
    )

    tables: Optional[List[Dict[str, Any]]] = Field(
        default=None, description="Extracted tables from the document"
    )

    images: Optional[List[Dict[str, Any]]] = Field(
        default=None, description="Information about images found in the document"
    )

    processed_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when processing was completed",
    )

    confidence_score: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Confidence score of the extraction (0.0 to 1.0)",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "success",
                "data": {
                    "transactions": [
                        {
                            "date": "2024-01-01",
                            "amount": 100.50,
                            "description": "Payment",
                        }
                    ]
                },
                "metadata": {"file_size": 1024, "format": "PDF", "version": "1.7"},
                "processor_type": "pdf",
                "processing_time_ms": 1250.5,
                "errors": None,
                "warnings": ["Some formatting may be lost"],
                "extracted_text": "Sample document text...",
                "page_count": 5,
                "tables": [{"rows": 10, "columns": 5}],
                "images": [{"page": 1, "format": "jpeg"}],
                "confidence_score": 0.95,
            }
        }
    )
