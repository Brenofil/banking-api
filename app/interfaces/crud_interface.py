"""
CRUD Interface for generic data operations.

This interface defines the contract for Create, Read, Update, and Delete operations
that can be implemented for databases, file systems, or any other storage mechanism.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional


class CrudInterface(ABC):
    """
    Abstract base class defining generic CRUD operations.

    This interface can be implemented for various storage mechanisms including:
    - Database repositories (SQL, NoSQL)
    - File system operations
    - Cloud storage services
    - In-memory caches

    All parameters are passed through **kwargs to maintain flexibility across
    different implementations.
    """

    @abstractmethod
    def create(self, **kwargs) -> Any:
        """
        Create a new resource.

        Args:
            **kwargs: Implementation-specific parameters
                     Examples:
                     - File operations: filename, content, directory
                     - Database: model, data, table_name
                     - Cloud storage: bucket, key, content

        Returns:
            Any: Implementation-specific return value (e.g., file path, record ID, URL)

        Raises:
            Exception: Implementation-specific exceptions
        """
        pass

    @abstractmethod
    def read(self, **kwargs) -> Any:
        """
        Read an existing resource.

        Args:
            **kwargs: Implementation-specific parameters
                     Examples:
                     - File operations: filename, directory
                     - Database: id, filters, table_name
                     - Cloud storage: bucket, key

        Returns:
            Any: Implementation-specific return value (e.g., file content, record, object)

        Raises:
            Exception: Implementation-specific exceptions
        """
        pass

    @abstractmethod
    def update(self, **kwargs) -> Any:
        """
        Update an existing resource.

        Args:
            **kwargs: Implementation-specific parameters
                     Examples:
                     - File operations: filename, content, directory
                     - Database: id, data, table_name
                     - Cloud storage: bucket, key, content

        Returns:
            Any: Implementation-specific return value (e.g., updated path, record, status)

        Raises:
            Exception: Implementation-specific exceptions
        """
        pass

    @abstractmethod
    def delete(self, **kwargs) -> bool:
        """
        Delete an existing resource.

        Args:
            **kwargs: Implementation-specific parameters
                     Examples:
                     - File operations: filename, directory
                     - Database: id, table_name
                     - Cloud storage: bucket, key

        Returns:
            bool: True if deletion was successful, False otherwise

        Raises:
            Exception: Implementation-specific exceptions
        """
        pass

    @abstractmethod
    def exists(self, **kwargs) -> bool:
        """
        Check if a resource exists.

        Args:
            **kwargs: Implementation-specific parameters
                     Examples:
                     - File operations: filename, directory
                     - Database: id, table_name
                     - Cloud storage: bucket, key

        Returns:
            bool: True if resource exists, False otherwise
        """
        pass

    @abstractmethod
    def list(self, **kwargs) -> list[Any]:
        """
        List resources based on criteria.

        Args:
            **kwargs: Implementation-specific parameters
                     Examples:
                     - File operations: directory, pattern, recursive
                     - Database: table_name, filters, limit
                     - Cloud storage: bucket, prefix

        Returns:
            list[Any]: List of resources (type depends on implementation)

        Raises:
            Exception: Implementation-specific exceptions
        """
        pass
