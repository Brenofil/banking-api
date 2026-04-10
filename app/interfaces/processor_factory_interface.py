from abc import ABC, abstractmethod
from typing_extensions import Optional, List

from app.interfaces.processor_interface import ProcessorInterface


class ProcessorFactoryInterface(ABC):
    """
    Processor Factory interface for processor factories.
    Each factory implementation follows the [factory method](https://refactoring.guru/design-patterns/factory-method) design pattern, also know as Virtual Constructor.

    This pattern provides an interface for creating objects but allows subclasses to alter the type of objects that will be created.
    In this application, factories are responsible for creating appropriate document processors based on file type, MIME type, or file extension.
    """

    @abstractmethod
    def create_processor(self, file_type: str) -> ProcessorInterface:
        """
        Factory method to create a processor for a specific file type.
        This is the core factory method that subclasses must implement to create
        the appropriate processor instance based on the file type.
        Args:
            file_type: File type identifier (e.g., 'pdf', 'csv', 'xlsx', 'docx')
        Returns:
            ProcessorInterface: Appropriate processor instance for the file type
        Raises:
            ValueError: If file_type is not supported
            NotImplementedError: If processor for file_type is not implemented
        Example:
            >>> factory = DocumentProcessorFactory()
            >>> processor = factory.create_processor('pdf')
            >>> result = processor.process(document_data)
        """
        pass

    @abstractmethod
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
        Example:
            >>> factory = DocumentProcessorFactory()
            >>> processor = factory.get_processor_by_extension('.pdf')
        """
        pass

    @abstractmethod
    def get_processor_by_mime_type(self, mime_type: str) -> ProcessorInterface:
        """
        Create a processor based on MIME type.
        Args:
            mime_type: MIME type (e.g., 'application/pdf', 'text/csv')
        Returns:
            ProcessorInterface: Appropriate processor instance
        Raises:
            ValueError: If MIME type is not supported
        Example:
            >>> factory = DocumentProcessorFactory()
            >>> processor = factory.get_processor_by_mime_type('application/pdf')
        """
        pass

    @abstractmethod
    def get_supported_types(self) -> List[str]:
        """
        Get list of all supported file types.
        Returns:
            List[str]: List of supported file type identifiers (e.g., ['pdf', 'csv', 'xlsx'])
        Example:
            >>> factory = DocumentProcessorFactory()
            >>> types = factory.get_supported_types()
            >>> print(types)  # ['pdf', 'csv', 'xlsx', 'docx']
        """
        pass

    @abstractmethod
    def is_supported(self, file_type: str) -> bool:
        """
        Check if a file type is supported by this factory.
        Args:
            file_type: File type identifier to check
        Returns:
            bool: True if file type is supported, False otherwise
        Example:
            >>> factory = DocumentProcessorFactory()
            >>> if factory.is_supported('pdf'):
            ...     processor = factory.create_processor('pdf')
        """
        pass

    def register_processor(self, file_type: str, processor_class: type) -> None:
        """
        Register a new processor type with the factory (optional).
        This method can be overridden by subclasses to support dynamic
        processor registration at runtime.
        Args:
            file_type: File type identifier
            processor_class: Processor class to register
        Example:
            >>> factory = DocumentProcessorFactory()
            >>> factory.register_processor('custom', CustomProcessor)
        """
        raise NotImplementedError("Dynamic processor registration not supported")

    def get_processor_info(self, file_type: str) -> Optional[dict]:
        """
        Get information about a specific processor type (optional).
        Can be overridden to provide metadata about available processors.
        Args:
            file_type: File type identifier
        Returns:
            Optional[dict]: Processor information including supported extensions,
                          MIME types, and capabilities, or None if not available
        Example:
            >>> factory = DocumentProcessorFactory()
            >>> info = factory.get_processor_info('pdf')
            >>> print(info)
            {
                'type': 'pdf',
                'extensions': ['.pdf'],
                'mime_types': ['application/pdf'],
                'capabilities': ['text_extraction', 'table_extraction']
            }
        """
        return None
