from datetime import datetime
from typing import Any, Dict, Optional
from fastapi import HTTPException, UploadFile, status
from app.constants.file_size import FileSizeContants
from app.interfaces.processor_interface import ProcessorInterface
from app.models.documents.processor import ProcessorResponse
from app.processors.factory import DocumentProcessorFactory
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
    ) -> ProcessorResponse:

        filename: str = file.filename or "documento"

        try:
            # [OK] 1. Validates file size and content
            self.logger.info("[1|5] reading file content")
            content: bytes = await self.read_from_file(file)

            # [OK] 2. Determines
            self.logger.info("[2|5] identifying appropriate processor")
            processor: ProcessorInterface = self._identify_processor(filename)

            # [OK] 3. Preprocesses the document
            self.logger.info("[3|5] Preprocessing document content")

            processed: ProcessorResponse = self.process_content(
                processor, content, password
            )

            # [OK] 4. Processes and extracts structured data using Docling
            self.logger.info("[4|5] Processing and extracting data with Docling")

            if processed.data and "dataframes" in processed.data:
                self._handle_dataframes(filename, processed.data)
            else:
                self.logger.info("No dataframes available in document")

            # [OK] 6. Returns complete processing results
            self.logger.info("[5|5] Returning processment results")

            return processed
        except Exception as e:
            self.logger.error(f"Unable to process document due to {str(e)}")
            raise e

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
                detail=f"File size exceeds maximum allowed size of {FileSizeContants.MAX_FILE_SIZE_MB}MB or file is empty",
            )

            raise http_exception

        self.logger.info(f"Finished reading file {file.filename}")

        return content

    def process_content(
        self,
        processor: ProcessorInterface,
        content: bytes,
        password: Optional[str] = None,
    ) -> ProcessorResponse:
        """
        _summary_

        Args:
            processor (ProcessorInterface): _description_
            content (bytes): _description_
            password (Optional[str], optional): _description_. Defaults to None.

        Returns:
            ProcessorResponse: _description_
        """
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

        return data
