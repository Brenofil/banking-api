import os


class FileConstants:

    # Get max file size from environment variable (default: 10 MB)
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
    MAX_FILE_SIZE_BYTES: int = MAX_FILE_SIZE_MB * 1024 * 1024

    # Get Output file directory
    OUTPUT_HTML_DIR: str = os.getenv("OUTPUT_HTML_DIR", "output/html")
    OUTPUT_JSON_DIR: str = os.getenv("OUTPUT_JSON_DIR", "output/json")
    OUTPUT_EXCEL_DIR: str = os.getenv("OUTPUT_EXCEL_DIR", "output/excel")
    OUTPUT_MARKDOWN_DIR: str = os.getenv("OUTPUT_MARKDOWN_DIR", "output/markdown")
