"""Logging levels enum for the logging service."""

from enum import Enum


class LoggingLevels(str, Enum):
    """
    Standard logging levels for the application logging service.

    These levels follow the standard logging hierarchy from most verbose to least verbose.
    Each level includes all messages from higher severity levels.

    Attributes:
        TRACE: Most detailed information, typically only for diagnosing problems.
               Use for tracing code execution flow and variable values.
               Example: "Entering function calculate_total with args: [1, 2, 3]"

        DEBUG: Detailed information useful during development and debugging.
               Use for diagnostic information that helps understand application behavior.
               Example: "Database query executed: SELECT * FROM users WHERE id=123"

        INFO: General informational messages about application progress and state.
              Use for normal application events and milestones.
              Example: "User logged in successfully", "Document processed"

        SUCCESS: Successful completion of operations (loguru-specific level).
                 Use to highlight successful outcomes of important operations.
                 Example: "Payment processed successfully", "File uploaded"

        WARNING: Indication of potential issues or unexpected situations.
                 Application continues but attention may be needed.
                 Example: "API rate limit approaching", "Deprecated function used"

        ERROR: Error events that might still allow the application to continue.
               Use for recoverable errors that don't crash the application.
               Example: "Failed to process document, retrying", "Invalid user input"

        CRITICAL: Very severe error events that might cause application termination.
                  Use for unrecoverable errors requiring immediate attention.
                  Example: "Database connection lost", "Out of memory"

    Usage:
        from enums.logging_levels import LoggingLevels
        from services.utils.logger import initialize_logger

        # Initialize logger with specific level
        initialize_logger(log_level=LoggingLevels.DEBUG.value)

        # Or use string directly
        initialize_logger(log_level="INFO")
    """

    TRACE = "TRACE"
    DEBUG = "DEBUG"
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
