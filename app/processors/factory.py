"""Document processor factory implementation."""

from typing import List, Optional

from app.interfaces.processor_factory_interface import ProcessorFactoryInterface
from app.interfaces.processor_interface import ProcessorInterface
from app.enums.file_extensions import FileExtension
from app.enums.mime_types import MimeType
from app.processors.pdf_processor import PdfDocumentProcessor


class DocumentProcessorFactory(ProcessorFactoryInterface):
    """
    Concrete implementation of the Processor Factory.

    This factory creates appropriate document processors based on file type,
    extension, or MIME type. It follows the Factory Method design pattern,
    providing a centralized way to instantiate processors without exposing
    the instantiation logic to clients.

    The factory maintains a registry of processor classes mapped to their
    supported file types, allowing for easy extension and modification.

    Example:
        >>> factory = DocumentProcessorFactory()
        >>> processor = factory.create_processor('pdf')
        >>> result = processor.process(document_bytes)
    """

    def __init__(self):
        """Initialize the factory with processor registry."""
        # Registry mapping file types to processor classes
        # This will be populated as processors are implemented
        self._processor_registry: dict[str, type[ProcessorInterface]] = {
            "pdf": PdfDocumentProcessor
            # TODO :: add other processors
        }

    def create_processor(self, file_type: str) -> ProcessorInterface:
        """
        Factory method to create a processor for a specific file type.

        Args:
            file_type: File type identifier (e.g., 'pdf', 'csv', 'xlsx', 'docx')

        Returns:
            ProcessorInterface: Appropriate processor instance for the file type

        Raises:
            ValueError: If file_type is not supported
            NotImplementedError: If processor for file_type is not implemented yet
        """

        file_type_lower = file_type.lower().strip()

        if not self.is_supported(file_type_lower):
            raise ValueError(
                f"Unsupported file type: {file_type}. "
                f"Supported types: {', '.join(self.get_supported_types())}"
            )

        processor_class = self._processor_registry.get(file_type_lower)

        if processor_class is None:
            raise NotImplementedError(
                f"Processor for file type '{file_type}' is not implemented yet. "
                f"The file type is recognized but no processor class has been registered."
            )

        return processor_class()

    def get_processor_by_extension(self, extension: str) -> ProcessorInterface:
        """
        Create a processor based on file extension.

        Args:
            extension: File extension (e.g., '.pdf', '.csv', '.xlsx')
                      Can be with or without leading dot

        Returns:
            ProcessorInterface: Appropriate processor instance

        Raises:
            ValueError: If extension is not supported
        """

        try:
            # Normalize extension using FileExtension enum and get file type
            file_ext = FileExtension.from_string(extension)
            file_type = file_ext.get_file_type()
            return self.create_processor(file_type)
        except ValueError as e:
            raise ValueError(
                f"Unsupported file extension: {extension}. "
                f"Supported extensions: {', '.join(FileExtension.get_all_extensions())}"
            ) from e

    def get_processor_by_mime_type(self, mime_type: str) -> ProcessorInterface:
        """
        Create a processor based on MIME type.

        Args:
            mime_type: MIME type (e.g., 'application/pdf', 'text/csv')

        Returns:
            ProcessorInterface: Appropriate processor instance

        Raises:
            ValueError: If MIME type is not supported
        """
        try:
            # Normalize MIME type using MimeType enum and get file type
            mime_enum = MimeType.from_string(mime_type)
            file_type = mime_enum.get_file_type()
            return self.create_processor(file_type)
        except ValueError as e:
            raise ValueError(
                f"Unsupported MIME type: {mime_type}. "
                f"Supported MIME types: {', '.join(MimeType.get_all_mime_types())}"
            ) from e

    def get_supported_types(self) -> List[str]:
        """
        Get list of all supported file types.

        Returns:
            List[str]: List of supported file type identifiers (e.g., ['pdf', 'csv', 'xlsx'])
        """
        # Get unique file types from FileExtension enum
        return sorted(set(FileExtension.get_extension_to_type_map().values()))

    def is_supported(self, file_type: str) -> bool:
        """
        Check if a file type is supported by this factory.

        Args:
            file_type: File type identifier to check

        Returns:
            bool: True if file type is supported, False otherwise
        """
        return file_type.lower().strip() in self.get_supported_types()

    def register_processor(self, file_type: str, processor_class: type) -> None:
        """
        Register a new processor type with the factory.

        This method allows dynamic processor registration at runtime,
        enabling extensibility without modifying the factory code.

        Args:
            file_type: File type identifier
            processor_class: Processor class to register (must implement ProcessorInterface)

        Raises:
            TypeError: If processor_class doesn't implement ProcessorInterface
            ValueError: If file_type is not in supported types
        """
        # Validate that the processor class implements ProcessorInterface
        if not issubclass(processor_class, ProcessorInterface):
            raise TypeError(
                f"Processor class must implement ProcessorInterface. "
                f"Got: {processor_class.__name__}"
            )

        file_type_lower = file_type.lower().strip()

        # Validate that file type is in supported types
        if file_type_lower not in self.get_supported_types():
            raise ValueError(
                f"Cannot register processor for unsupported file type: {file_type}. "
                f"Supported types: {', '.join(self.get_supported_types())}"
            )

        self._processor_registry[file_type_lower] = processor_class

    def get_processor_info(self, file_type: str) -> Optional[dict]:
        """
        Get information about a specific processor type.

        Provides metadata about available processors including supported
        extensions, MIME types, and capabilities.

        Args:
            file_type: File type identifier

        Returns:
            Optional[dict]: Processor information including supported extensions,
                          MIME types, and capabilities, or None if not available
        """
        file_type_lower = file_type.lower().strip()

        if not self.is_supported(file_type_lower):
            return None

        # Get extension and MIME type maps from enums
        extension_map = FileExtension.get_extension_to_type_map()
        mime_map = MimeType.get_mime_to_type_map()

        # Find extensions for this file type
        extensions = [
            ext for ext, ftype in extension_map.items() if ftype == file_type_lower
        ]

        # Find MIME types for this file type
        mime_types = [
            mime for mime, ftype in mime_map.items() if ftype == file_type_lower
        ]

        # Check if processor is implemented
        is_implemented = file_type_lower in self._processor_registry

        return {
            "type": file_type_lower,
            "extensions": extensions,
            "mime_types": mime_types,
            "implemented": is_implemented,
        }
