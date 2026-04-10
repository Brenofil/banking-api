"""
Document processing endpoints
"""

import os
from typing import Optional

from fastapi import APIRouter, HTTPException, status, UploadFile, File

from app.interfaces.processor_interface import ProcessorInterface
from app.models.documents.document import DocumentProcessingResponse
from app.services.utils.logger import LoggerService
from app.services.documents.processors.factory import DocumentProcessorFactory

router = APIRouter()

# Get max file size from environment variable (default: 10 MB)
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

logger = LoggerService().get_logger("Document Route")


@router.post(
    "/upload",
    response_model=DocumentProcessingResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a document for processing

    - file: Document file to upload (max size configurable via MAX_FILE_SIZE_MB env var)
    """
    # Read file content to check size
    content = await file.read()
    file_size = len(content)

    # Validate file size
    if file_size > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size ({file_size / (1024 * 1024):.2f} MB) exceeds maximum allowed size ({MAX_FILE_SIZE_MB} MB)",
        )

    # Validate file is not empty
    if file_size == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="File is empty"
        )

    try:
        factory: DocumentProcessorFactory = DocumentProcessorFactory()
        logger.debug("Instantiated document processor factory")

        logger.info("File has content_type :: %s", file.content_type)

    except Exception as e:
        logger.error("Failed to process document, error: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process document: {str(e)}",
        )

    logger.warning("For now, just returning success response")

    return DocumentProcessingResponse(
        filename=file.filename or "unknown",
        size_bytes=file_size,
        content_type=file.content_type,
        status="success",
        message=f"Document uploaded successfully. Size: {file_size / 1024:.2f} KB",
    )


@router.get("/config")
async def get_processing_config():
    """Get current processing configuration"""
    return {
        "max_file_size_mb": MAX_FILE_SIZE_MB,
        "max_file_size_bytes": MAX_FILE_SIZE_BYTES,
    }
