from datetime import datetime
from typing import Any, Dict, Optional
from fastapi import HTTPException, UploadFile, status
from app.interfaces.processor_interface import ProcessorInterface
from app.models.documents.processor import ProcessorResponse
from app.processors.factory import DocumentProcessorFactory
from app.routers.documents import MAX_FILE_SIZE_MB
from app.services.base_service import BaseService
from app.utils.file_operations import FileOperations
import pandas as pd


class DocumentProcessorService(BaseService):
    """
    Service responsible for executing the processment pipeline for a document.
    """

    file_operations: FileOperations = FileOperations()
    factory: DocumentProcessorFactory = DocumentProcessorFactory()

    def __init__(self) -> None:
        pass

    async def process_document(
        self, file: UploadFile, password: Optional[str] = None
    ) -> None:
        # TODO :: add a try catch to execute the pipeline,
        # only them it should register start, success or error

        filename: str = file.filename or "documento"

        # [OK] 1. Validates file size and content
        self.logger.info("[1|6] reading file content")
        content: bytes = await self.read_from_file(file)
        # [OK] 2. Determines
        self.logger.info("[2|6] identifying appropriate processor")
        processor: ProcessorInterface = self._identify_processor(filename)
        # [OK] 3. Preprocesses the document
        self.logger.info("[3|6] Preprocessing document content")

        processed: ProcessorResponse = self.preprocess_document_content(
            processor, content, password
        )

        # self._handle_dataframes(filename, processed.data)
        # 4. Processes and extracts structured data using Docling
        self.logger.info("[4|6] Processing and extracting data with Docling")
        # 5. Handles password-protected documents (e.g., encrypted PDFs)
        self.logger.info("[5|6] Handling password-protected documents")
        # 6. Returns complete processing results
        self.logger.info("[6|6] Returning processment results")

        pass

    async def read_from_file(self, file: UploadFile) -> bytes:
        """_summary_

        Args:
            file (UploadFile): _description_

        Returns:
            bytes: _description_
        """
        try:
            content: bytes = await file.read()
        except Exception as error:
            raise error

        # Validates file size
        valid_size: bool = self.file_operations.validate_size(content)

        if not valid_size:
            self.logger.error(f"File {file.filename} could not be processed")

            http_exception: HTTPException = HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File size exceeds maximum allowed size of {MAX_FILE_SIZE_MB}MB or file is empty",
            )

            raise http_exception

        self.logger.info(f"Finished reading file {file.filename}")

        return content

    def preprocess_document_content(
        self,
        processor: ProcessorInterface,
        content: bytes,
        password: Optional[str] = None,
    ) -> ProcessorResponse:

        if password:
            self.logger.info("Password provided for encrypted document processing")

        processed: ProcessorResponse = processor.process(content, password)

        # Log processing results
        self.logger.info(
            f"Document processed successfully - "
            f"Status: {processed.status}, "
            f"Processing time: {processed.processing_time_ms:.2f}ms, "
            f"Pages: {processed.page_count}, "
            f"Tables: {len(processed.tables) if processed.tables else 0}"
        )

        return processed

    def process_document_content(self) -> None:
        pass

    def _identify_processor(self, filename: Optional[str] = None) -> ProcessorInterface:
        """
        Method responsible for identifying the processor for a specific type of document

        Args:
            filename (Optional[str], optional): the document's name. Defaults to None.

        Returns:
            ProcessorInterface: the processor responsible for processing the identified type of document
        """

        if not filename or "." not in filename:
            raise ValueError("Invalid filename - no extension found")

        extension: str = filename.split(".")[-1]
        self.logger.debug(f"Detected file extensions: .{extension}")

        # Get appropriate processor
        processor: ProcessorInterface = self.factory.get_processor_by_extension(
            extension
        )

        self.logger.info(f"Using processor: {processor.getName()}")
        return processor

    def _handle_dataframes(
        self, filename: str = "document", data: Dict[str, Any] = {}
    ) -> Dict[str, Any]:
        """
        Method responsible for generating excel files with the dataframes available from processed content in a document

        Args:
            filename (str, optional): The document's name. Defaults to "document".
            data (Dict[str, Any], optional): The document's data, which contains the dataframes. Defaults to {}.

        Returns:
            Dict[str, Any]: A dictionary with the DataFrames and previous data from the document processment pipeline
        """

        if data and "dataframes" in data:
            self.logger.debug("Handling dataframes from processor response")
            try:
                dataframe_data = data["dataframes"]

                # Reconstructr DataFrames from serialized format
                dataframes = [
                    pd.DataFrame(df["data"])
                    for df in (
                        dataframe_data
                        if isinstance(dataframe_data, list)
                        else [dataframe_data]
                    )
                ]

                # Generate filename with timestamp
                timestamp: str = datetime.now().strftime("%Y%m%d_%H%M%S")
                base_filename: str = filename.rsplit(".", 1)[0]

                excel_filename: str = f"{base_filename}_{timestamp}_tables.xlsx"

                # Save to file
                saved_path: str = self.file_operations.create(
                    filename=excel_filename, content=dataframes, overwrite=True
                )

                data["excel_file"] = saved_path
                self.logger.info(f"Saved DataFrames to Excel file @ {saved_path}")

            except Exception as e:
                self.logger.error(f"Failed to save DataFrames to Excel: {str(e)}")
                # Don't raise exception, just log the warning
        else:
            self.logger.warning("No dataframes available in processor response")

        return data
