"""
Document processing endpoints available for this API, for now the endpoints
available are:

1. /upload :: responsible for uploading a document for processing
2. /config :: responsible for returning the current processing configuration

Other endpoints will be developed as needed
"""

import os
from typing import Optional
from datetime import datetime
import pandas as pd

from app.utils.logger import LoggerService
from app.utils.file_operations import FileOperations
from app.processors.factory import DocumentProcessorFactory
from app.models.documents.processor import ProcessorResponse
from app.interfaces.processor_interface import ProcessorInterface
from app.models.documents.document import DocumentProcessingResponse
from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form

router = APIRouter()

# Get max file size from environment variable (default: 10 MB)
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

logger = LoggerService().get_logger("Document Route")


@router.post(
    "/upload",
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

    content: bytes = await file.read()
    file_size: int = len(content)

    # Validate file size
    if file_size > MAX_FILE_SIZE_BYTES:
        logger.error(f"File size {file_size} exceeds maximum {MAX_FILE_SIZE_BYTES}")
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size ({file_size / (1024 * 1024):.2f} MB) exceeds maximum allowed size ({MAX_FILE_SIZE_MB} MB)",
        )

    # Validate empty files
    if file_size == 0:
        logger.error("Empty file received")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="File is empty"
        )

    try:
        logger.info("Instantiating document processor factory")
        factory: DocumentProcessorFactory = DocumentProcessorFactory()

        # Extract file extension
        if not file.filename or "." not in file.filename:
            raise ValueError("Invalid filename - no extension found")

        extension: str = file.filename.split(".")[-1]
        logger.info(f"Detected file extension: .{extension}")

        # Get appropriate processor
        processor: ProcessorInterface = factory.get_processor_by_extension(extension)
        logger.info(f"Using processor: {processor.getName()}")

        # Process document through complete pipeline
        logger.info("Starting document processing pipeline")
        if password:
            logger.info("Password provided for encrypted document processing")

        # Process: preprocess, extract structured data using Docling, and postprocess
        # Note: The processor.process() method handles preprocessing internally
        logger.info(
            "Processing document (includes preprocessing, extraction, and postprocessing)"
        )
        response: ProcessorResponse = processor.process(content, password=password)

        # Log processing results
        logger.info(
            f"Document processed successfully - "
            f"Status: {response.status}, "
            f"Processing time: {response.processing_time_ms:.2f}ms, "
            f"Pages: {response.page_count}, "
            f"Tables: {len(response.tables) if response.tables else 0}"
        )

        # Save DataFrames to Excel file if available
        if response.data and "dataframes" in response.data:
            try:
                dataframes_data = response.data["dataframes"]

                # Reconstruct DataFrames from serialized format
                if isinstance(dataframes_data, list):
                    # Multiple DataFrames
                    dataframes = [
                        pd.DataFrame(df_data["data"]) for df_data in dataframes_data
                    ]
                else:
                    # Single DataFrame
                    dataframes = pd.DataFrame(dataframes_data["data"])

                # Generate filename with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                base_filename = (
                    file.filename.rsplit(".", 1)[0] if file.filename else "document"
                )
                excel_filename = f"{base_filename}_{timestamp}_tables.xlsx"

                # Save to file using FileOperations
                file_ops = FileOperations()
                saved_path = file_ops.create(
                    filename=excel_filename, content=dataframes, overwrite=True
                )

                # Add file path to response
                response.data["excel_file"] = saved_path
                logger.info(f"Saved DataFrames to Excel file: {saved_path}")

            except Exception as e:
                logger.warning(f"Failed to save DataFrames to Excel: {str(e)}")
                # Don't fail the request, just log the warning

        return response

    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid request: {str(e)}",
        )
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
        "max_file_size_mb": MAX_FILE_SIZE_MB,
        "max_file_size_bytes": MAX_FILE_SIZE_BYTES,
    }
