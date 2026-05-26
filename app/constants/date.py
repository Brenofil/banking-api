import os


class DateConstants:

    DEFAULT_FORMAT: str = os.getenv("DATE_FORMAT", "yyyy-mm-dd")
    XLSX_FORMAT: str = os.getenv("XLSX_DATE_FORMAT", "YYYY-MM-DD")

    # TIME FORMATS
    TIME_STAMP: str = os.getenv("TIME_STAMP_FORMAT", "%Y%m%d_%H%M%S")
