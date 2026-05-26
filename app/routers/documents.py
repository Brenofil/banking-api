"""
Document processing endpoints available for this API, for now the endpoints
available are:

1. /upload :: responsible for uploading a document for processing
2. /config :: responsible for returning the current processing configuration

Other endpoints will be developed as needed
"""

from typing import Optional
from datetime import datetime
import pandas as pd

from app.utils.logger import get_logger
from app.constants.files import FileConstants
from app.services.documents.processor import DocumentProcessorService
from app.models.documents.processor import ProcessorResponse
from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form

router = APIRouter()

logger = get_logger("Document Route")

doc_processor: DocumentProcessorService = DocumentProcessorService()


@router.post(
    "/process",
    response_model=ProcessorResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(
    file: UploadFile = File(..., description="Document file to upload and process"),
    password: Optional[str] = Form(
        None,
        description="Password for encrypted/protected documents (e.g., banking PDFs with sensitive information)",
    ),
) -> ProcessorResponse:
    """
    Upload and process a document through the complete pipeline.

    This endpoint:
    1. Validates file size and content
    2. Determines appropriate processor based on file extension
    3. Preprocesses the document
    4. Processes and extracts structured data using Docling
    5. Handles password-protected documents (e.g., encrypted PDFs)
    6. Returns complete processing results

    Args:
        file: Document file to upload (max size configurable via MAX_FILE_SIZE_MB env var)
        password: Optional password for encrypted/protected documents (e.g., banking PDFs with credit card info)

    Returns:
        ProcessorResponse: Complete processing results including extracted data,
                          metadata, tables, images, and processing statistics

    Note:
        For banking documents with sensitive information (credit cards, account numbers),
        PDFs are often password-protected. Provide the password parameter to process
        these encrypted documents.
    """

    logger.info(f"Received document upload request: {file.filename}")

    try:
        logger.debug("Starting document processing pipeline")

        return await doc_processor.process_document(file, password)
    except Exception as e:
        logger.error(f"Failed to process document: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process document: {str(e)}",
        )


@router.get("/config")
async def get_processing_config():
    """Get current processing configuration"""
    return {
        "max_file_size_mb": FileConstants.MAX_FILE_SIZE_MB,
        "max_file_size_bytes": FileConstants.MAX_FILE_SIZE_BYTES,
    }
