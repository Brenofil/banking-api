"""
Logging service using loguru for structured and beautiful logging.

This module provides a centralized logging configuration for the application,
with support for file rotation, different log levels, and structured logging.

Features:
    - Colored console output with syntax highlighting
    - Automatic file rotation based on size or time
    - Separate error log file with full tracebacks
    - Thread-safe logging operations
    - Structured logging with context binding
    - Request and processor-specific logging helpers

Usage:
    # Initialize at application startup (e.g., in main.py)
    from services.utils.logger import initialize_logger, get_logger
    from enums.logging_levels import LoggingLevels

    initialize_logger(
        log_dir="logs",
        log_level=LoggingLevels.INFO.value,
        rotation="10 MB",
        retention="30 days"
    )

    # Use in any class - automatically shows class name
    class DocumentProcessor:
        def __init__(self):
            self.logger = get_logger()  # Automatically detects class name

        def process(self):
            self.logger.info("Processing document")  # Shows: DocumentProcessor | ...
            self.logger.bind(doc_id="123").info("Document processed")

    # Or use manually with custom name
    logger = get_logger("custom_service")
    logger.info("Application started")

Log Files:
    - logs/app_YYYY-MM-DD.log: General application logs
    - logs/errors_YYYY-MM-DD.log: Error and critical logs with full tracebacks
"""

import inspect
import os
import sys
from pathlib import Path
from typing import Optional, Union

from loguru import logger

from app.enums.logging_levels import LoggingLevels


def _get_caller_class_name() -> Optional[str]:
    """
    Automatically detect the calling class name using stack inspection.

    Returns:
        Class name if called from within a class method, None otherwise
    """
    frame = inspect.currentframe()
    try:
        if frame is None:
            return None

        # Go up the stack to find the caller
        # Skip: _get_caller_class_name -> get_logger -> caller
        caller_frame = frame.f_back
        if caller_frame is None:
            return None
        caller_frame = caller_frame.f_back
        if caller_frame is None:
            return None
        caller_frame = caller_frame.f_back
        if caller_frame is None:
            return None

        # Get the 'self' or 'cls' from the caller's local variables
        caller_locals = caller_frame.f_locals

        # Check for 'self' (instance method)
        if "self" in caller_locals:
            return caller_locals["self"].__class__.__name__

        # Check for 'cls' (class method)
        if "cls" in caller_locals:
            return caller_locals["cls"].__name__

        return None
    finally:
        del frame


class LoggerService:
    """
    Centralized logging service using loguru.

    Features:
    - Colored console output for better readability
    - File rotation with size and time-based rotation
    - Structured logging with context
    - Different log levels for different outputs
    - Request ID tracking for API calls
    """

    def __init__(
        self,
        log_dir: str = "logs",
        rotation: str = "10 MB",
        retention: str = "30 days",
        compression: str = "zip",
    ):
        """
        Initialize the logging service with custom configuration.

        Args:
            log_dir: Directory to store log files (default: "logs")
            rotation: When to rotate log files. Examples:
                     - "10 MB": Rotate when file reaches 10 megabytes
                     - "1 day": Rotate daily at midnight
                     - "1 week": Rotate weekly
                     - "00:00": Rotate at midnight
                     (default: "10 MB")
            retention: How long to keep old log files. Examples:
                      - "30 days": Keep logs for 30 days
                      - "1 week": Keep logs for 1 week
                      - "10": Keep last 10 rotated files
                      (default: "30 days")
            compression: Compression format for rotated logs.
                        Options: "zip", "gz", "bz2", "xz"
                        (default: "zip")

        Example:
            >>> from enums.logging_levels import LoggingLevels
            >>> service = LoggerService(
            ...     log_dir="logs",
            ...     log_level=LoggingLevels.DEBUG.value,
            ...     rotation="5 MB",
            ...     retention="7 days",
            ...     compression="gz"
            ... )
        """
        # Convert LoggingLevels enum to string if needed
        self.log_dir = Path(log_dir)
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.rotation = rotation
        self.retention = retention
        self.compression = compression

        # Create log directory if it doesn't exist
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Remove default logger
        logger.remove()

        # Configure loggers
        self._configure_console_logger()
        self._configure_file_logger()
        self._configure_error_logger()

    def _configure_console_logger(self):
        """
        Configure colored console output for development.

        Outputs logs to stdout with:
        - Color-coded log levels
        - Timestamp in green
        - Class name (if available) in magenta
        - Module/function/line information in cyan
        - Message in level-specific color
        """
        logger.add(
            sys.stdout,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <magenta>{extra[class_name]}</magenta> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            level=self.log_level,
            colorize=True,
        )

    def _configure_file_logger(self):
        """
        Configure general file logger with rotation.

        Creates daily log files with:
        - Automatic rotation based on size or time
        - Compression of old logs
        - Thread-safe writing
        - Retention policy for old logs
        """
        logger.add(
            self.log_dir / "app_{time:YYYY-MM-DD}.log",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {extra[class_name]} | {name}:{function}:{line} - {message}",
            level=self.log_level,
            rotation=self.rotation,
            retention=self.retention,
            compression=self.compression,
            enqueue=True,  # Thread-safe logging
        )

    def _configure_error_logger(self):
        """
        Configure separate error logger for critical issues.

        Creates error-specific log files with:
        - Full exception tracebacks
        - Variable values at error point (diagnose=True)
        - Daily rotation
        - Only ERROR and CRITICAL level messages
        """
        logger.add(
            self.log_dir / "errors_{time:YYYY-MM-DD}.log",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {extra[class_name]} | {name}:{function}:{line} - {message}\n{extra}",
            level="ERROR",
            rotation="1 day",
            retention=self.retention,
            compression=self.compression,
            backtrace=True,  # Include full traceback
            diagnose=True,  # Include variable values
            enqueue=True,
        )

    def get_logger(self, name: Optional[str] = None):
        """
        Get a logger instance with optional context binding.

        If no name is provided, automatically detects the calling class name.

        Args:
            name: Optional service/module/class name to bind to the logger.
                 If not provided, automatically detects the calling class name.

        Returns:
            Logger instance with class_name context binding

        Example:
            >>> # Automatic class detection
            >>> class DocumentProcessor:
            ...     def __init__(self):
            ...         self.logger = service.get_logger()
            ...     def process(self):
            ...         self.logger.info("Processing")  # Shows: DocumentProcessor | ...
            >>>
            >>> # Manual name
            >>> logger = service.get_logger("custom_service")
            >>> logger.info("Processing")  # Shows: custom_service | ...
        """
        # Auto-detect class name if not provided
        if name is None:
            name = _get_caller_class_name() or "App"

        return logger.bind(class_name=name)

    @staticmethod
    def log_request(
        request_id: str, method: str, path: str, status_code: int, duration_ms: float
    ):
        """
        Log HTTP request with structured data for API monitoring.

        Args:
            request_id: Unique request identifier (e.g., UUID)
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            path: Request path (e.g., "/api/documents/process")
            status_code: HTTP status code (200, 404, 500, etc.)
            duration_ms: Request duration in milliseconds

        Example:
            >>> LoggerService.log_request(
            ...     request_id="req_abc123",
            ...     method="POST",
            ...     path="/api/documents",
            ...     status_code=201,
            ...     duration_ms=125.5
            ... )
        """
        logger.bind(
            request_id=request_id,
            method=method,
            path=path,
            status_code=status_code,
            duration_ms=duration_ms,
        ).info(f"{method} {path} - {status_code} ({duration_ms:.2f}ms)")

    @staticmethod
    def log_processor(processor_type: str, status: str, duration_ms: float, **kwargs):
        """
        Log document processor execution with performance metrics.

        Args:
            processor_type: Type of processor (pdf, csv, xlsx, etc.)
            status: Processing status (success, failed, partial_success, etc.)
            duration_ms: Processing duration in milliseconds
            **kwargs: Additional context data (e.g., page_count, file_size, error_count)

        Example:
            >>> LoggerService.log_processor(
            ...     processor_type="pdf",
            ...     status="success",
            ...     duration_ms=2500.0,
            ...     page_count=10,
            ...     file_size=1024000
            ... )
        """
        logger.bind(
            processor_type=processor_type,
            status=status,
            duration_ms=duration_ms,
            **kwargs,
        ).info(
            f"Processor {processor_type} completed with status {status} ({duration_ms:.2f}ms)"
        )

    @staticmethod
    def log_error(error: Exception, context: Optional[dict] = None):
        """
        Log error with full context and traceback for debugging.

        Args:
            error: Exception that occurred
            context: Additional context information (e.g., user_id, document_id, operation)

        Example:
            >>> try:
            ...     process_document(doc_id="123")
            ... except Exception as e:
            ...     LoggerService.log_error(e, context={
            ...         "document_id": "123",
            ...         "processor_type": "pdf",
            ...         "user_id": "user_456"
            ...     })
        """
        if context:
            logger.bind(**context).exception(f"Error occurred: {str(error)}")
        else:
            logger.exception(f"Error occurred: {str(error)}")


# Global logger service instance
_logger_service: Optional[LoggerService] = None


def initialize_logger(
    log_dir: str = "logs",
    log_level: Union[str, LoggingLevels] = "INFO",
    rotation: str = "10 MB",
    retention: str = "30 days",
    compression: str = "zip",
) -> LoggerService:
    """
    Initialize the global logger service for the application.

    This should be called once at application startup, typically in main.py.

    Args:
        log_dir: Directory to store log files (default: "logs")
        log_level: Minimum log level. Can be string or LoggingLevels enum (default: "INFO")
        rotation: When to rotate log files (default: "10 MB")
        retention: How long to keep old log files (default: "30 days")
        compression: Compression format for rotated logs (default: "zip")

    Returns:
        LoggerService instance

    Example:
        >>> from services.utils.logger import initialize_logger
        >>> from enums.logging_levels import LoggingLevels
        >>>
        >>> # In main.py
        >>> initialize_logger(
        ...     log_level=LoggingLevels.DEBUG.value,
        ...     rotation="5 MB",
        ...     retention="7 days"
        ... )
    """
    global _logger_service
    _logger_service = LoggerService(
        log_dir=log_dir,
        rotation=rotation,
        retention=retention,
        compression=compression,
    )
    return _logger_service


def get_logger(name: Optional[str] = None):
    """
    Get the global logger instance with optional context binding.

    If the logger service hasn't been initialized, it will be auto-initialized
    with default settings.

    Args:
        name: Optional service/module name to bind to the logger.
             This helps identify the source of log messages.

    Returns:
        Logger instance with optional context binding

    Example:
        >>> from services.utils.logger import get_logger
        >>>
        >>> # In any module
        >>> logger = get_logger("document_processor")
        >>> logger.info("Starting document processing")
        >>> logger.bind(doc_id="123").info("Processing document")
    """
    global _logger_service
    if _logger_service is None:
        # Auto-initialize with defaults if not already initialized
        _logger_service = initialize_logger()
    return _logger_service.get_logger(name)


# Convenience exports
__all__ = [
    "LoggerService",
    "initialize_logger",
    "get_logger",
    "logger",
    "LoggingLevels",
]
