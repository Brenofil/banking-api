"""
Unit tests for MimeType enum
"""

import pytest

from app.enums.mime_types import MimeType


class TestMimeType:
    """
    Test Suite for MimeType enum
    """

    def test_mime_type_values(self):
        """Test that all MIME type enum values are correct"""
        assert MimeType.PDF.value == "application/pdf"
        assert MimeType.CSV.value == "text/csv"
        assert (
            MimeType.XLSX.value
            == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        assert MimeType.XLS.value == "application/vnd.ms-excel"
        assert (
            MimeType.DOCX.value
            == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        assert MimeType.DOC.value == "application/msword"
        assert MimeType.TXT.value == "text/plain"
        assert MimeType.JSON.value == "application/json"
        assert MimeType.XML.value == "application/xml"
        assert MimeType.XML_TEXT.value == "text/xml"

    def test_get_file_type_for_all_mime_types(self):
        """Test get_file_type method for all MIME types"""
        assert MimeType.PDF.get_file_type() == "pdf"
        assert MimeType.CSV.get_file_type() == "csv"
        assert MimeType.XLSX.get_file_type() == "xlsx"
        assert MimeType.XLS.get_file_type() == "xls"
        assert MimeType.DOCX.get_file_type() == "docx"
        assert MimeType.DOC.get_file_type() == "doc"
        assert MimeType.TXT.get_file_type() == "txt"
        assert MimeType.JSON.get_file_type() == "json"
        assert MimeType.XML.get_file_type() == "xml"
        assert MimeType.XML_TEXT.get_file_type() == "xml"

    def test_get_mime_to_type_map(self):
        """Test get_mime_to_type_map class method"""
        mime_map = MimeType.get_mime_to_type_map()

        assert isinstance(mime_map, dict)
        assert mime_map["application/pdf"] == "pdf"
        assert mime_map["text/csv"] == "csv"
        assert (
            mime_map[
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            ]
            == "xlsx"
        )
        assert mime_map["application/vnd.ms-excel"] == "xls"
        assert (
            mime_map[
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            ]
            == "docx"
        )
        assert mime_map["application/msword"] == "doc"
        assert mime_map["text/plain"] == "txt"
        assert mime_map["application/json"] == "json"
        assert mime_map["application/xml"] == "xml"
        assert mime_map["text/xml"] == "xml"

    def test_from_file_type_valid_types(self):
        """Test from_file_type with valid file types"""
        assert MimeType.from_file_type("pdf") == MimeType.PDF
        assert MimeType.from_file_type("csv") == MimeType.CSV
        assert MimeType.from_file_type("xlsx") == MimeType.XLSX
        assert MimeType.from_file_type("xls") == MimeType.XLS
        assert MimeType.from_file_type("docx") == MimeType.DOCX
        assert MimeType.from_file_type("doc") == MimeType.DOC
        assert MimeType.from_file_type("txt") == MimeType.TXT
        assert MimeType.from_file_type("json") == MimeType.JSON
        assert MimeType.from_file_type("xml") == MimeType.XML

    def test_from_file_type_case_insensitive(self):
        """Test from_file_type is case insensitive"""
        assert MimeType.from_file_type("PDF") == MimeType.PDF
        assert MimeType.from_file_type("Csv") == MimeType.CSV
        assert MimeType.from_file_type("XLSX") == MimeType.XLSX

    def test_from_file_type_strips_whitespace(self):
        """Test from_file_type strips whitespace"""
        assert MimeType.from_file_type("  pdf  ") == MimeType.PDF
        assert MimeType.from_file_type("\tcsv\n") == MimeType.CSV

    def test_from_file_type_invalid_type_raises_error(self):
        """Test from_file_type raises ValueError for invalid type"""
        with pytest.raises(ValueError, match="Unknown file type: unknown"):
            MimeType.from_file_type("unknown")

    def test_from_string_valid_mime_types(self):
        """Test from_string with valid MIME types"""
        assert MimeType.from_string("application/pdf") == MimeType.PDF
        assert MimeType.from_string("text/csv") == MimeType.CSV
        assert (
            MimeType.from_string(
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            == MimeType.XLSX
        )
        assert MimeType.from_string("application/vnd.ms-excel") == MimeType.XLS
        assert (
            MimeType.from_string(
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
            == MimeType.DOCX
        )
        assert MimeType.from_string("application/msword") == MimeType.DOC
        assert MimeType.from_string("text/plain") == MimeType.TXT
        assert MimeType.from_string("application/json") == MimeType.JSON

    def test_from_string_xml_variants(self):
        """Test from_string handles both XML MIME types"""
        assert MimeType.from_string("application/xml") == MimeType.XML
        assert MimeType.from_string("text/xml") == MimeType.XML_TEXT

    def test_from_string_case_insensitive(self):
        """Test from_string is case insensitive"""
        assert MimeType.from_string("APPLICATION/PDF") == MimeType.PDF
        assert MimeType.from_string("Text/CSV") == MimeType.CSV

    def test_from_string_strips_whitespace(self):
        """Test from_string strips whitespace"""
        assert MimeType.from_string("  application/pdf  ") == MimeType.PDF
        assert MimeType.from_string("\ttext/csv\n") == MimeType.CSV

    def test_from_string_invalid_mime_type_raises_error(self):
        """Test from_string raises ValueError for unsupported MIME type"""
        with pytest.raises(
            ValueError, match="Unsupported MIME type: application/unknown"
        ):
            MimeType.from_string("application/unknown")

    def test_get_all_mime_types(self):
        """Test get_all_mime_types returns all MIME type values"""
        all_types = MimeType.get_all_mime_types()

        assert isinstance(all_types, list)
        assert len(all_types) == 10  # Total number of MIME types
        assert "application/pdf" in all_types
        assert "text/csv" in all_types
        assert (
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            in all_types
        )
        assert "application/vnd.ms-excel" in all_types
        assert (
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            in all_types
        )
        assert "application/msword" in all_types
        assert "text/plain" in all_types
        assert "application/json" in all_types
        assert "application/xml" in all_types
        assert "text/xml" in all_types

    def test_is_supported_with_valid_mime_types(self):
        """Test is_supported returns True for valid MIME types"""
        assert MimeType.is_supported("application/pdf") is True
        assert MimeType.is_supported("text/csv") is True
        assert MimeType.is_supported("application/json") is True
        assert MimeType.is_supported("application/xml") is True
        assert MimeType.is_supported("text/xml") is True

    def test_is_supported_with_invalid_mime_types(self):
        """Test is_supported returns False for invalid MIME types"""
        assert MimeType.is_supported("application/unknown") is False
        assert MimeType.is_supported("text/html") is False
        assert MimeType.is_supported("image/png") is False

    def test_is_supported_case_insensitive(self):
        """Test is_supported is case insensitive"""
        assert MimeType.is_supported("APPLICATION/PDF") is True
        assert MimeType.is_supported("Text/CSV") is True

    def test_get_mime_type_for_extension_valid_extensions(self):
        """Test get_mime_type_for_extension with valid extensions"""
        assert MimeType.get_mime_type_for_extension(".pdf") == MimeType.PDF
        assert MimeType.get_mime_type_for_extension(".csv") == MimeType.CSV
        assert MimeType.get_mime_type_for_extension(".xlsx") == MimeType.XLSX
        assert MimeType.get_mime_type_for_extension(".xls") == MimeType.XLS
        assert MimeType.get_mime_type_for_extension(".docx") == MimeType.DOCX
        assert MimeType.get_mime_type_for_extension(".doc") == MimeType.DOC
        assert MimeType.get_mime_type_for_extension(".txt") == MimeType.TXT
        assert MimeType.get_mime_type_for_extension(".json") == MimeType.JSON
        assert MimeType.get_mime_type_for_extension(".xml") == MimeType.XML

    def test_get_mime_type_for_extension_without_dot(self):
        """Test get_mime_type_for_extension works without leading dot"""
        assert MimeType.get_mime_type_for_extension("pdf") == MimeType.PDF
        assert MimeType.get_mime_type_for_extension("csv") == MimeType.CSV
        assert MimeType.get_mime_type_for_extension("xlsx") == MimeType.XLSX

    def test_get_mime_type_for_extension_case_insensitive(self):
        """Test get_mime_type_for_extension is case insensitive"""
        assert MimeType.get_mime_type_for_extension(".PDF") == MimeType.PDF
        assert MimeType.get_mime_type_for_extension("CSV") == MimeType.CSV
        assert MimeType.get_mime_type_for_extension(".XlSx") == MimeType.XLSX

    def test_get_mime_type_for_extension_strips_whitespace(self):
        """Test get_mime_type_for_extension strips whitespace"""
        assert MimeType.get_mime_type_for_extension("  .pdf  ") == MimeType.PDF
        assert MimeType.get_mime_type_for_extension("\tcsv\n") == MimeType.CSV

    def test_get_mime_type_for_extension_invalid_extension_raises_error(self):
        """Test get_mime_type_for_extension raises ValueError for invalid extension"""
        with pytest.raises(
            ValueError, match="No MIME type mapping for extension: .unknown"
        ):
            MimeType.get_mime_type_for_extension(".unknown")

    def test_mime_type_is_string_enum(self):
        """Test that MimeType inherits from str"""
        assert isinstance(MimeType.PDF, str)
        assert isinstance(MimeType.CSV, str)

    def test_mime_type_string_comparison(self):
        """Test that MimeType can be compared with strings"""
        assert MimeType.PDF == "application/pdf"
        assert MimeType.CSV == "text/csv"
        assert "application/pdf" == MimeType.PDF

    def test_mime_type_iteration(self):
        """Test that MimeType enum can be iterated"""
        mime_types = list(MimeType)
        assert len(mime_types) == 10
        assert MimeType.PDF in mime_types
        assert MimeType.CSV in mime_types

    def test_from_file_type_error_message_includes_known_types(self):
        """Test that from_file_type error message includes known types"""
        with pytest.raises(ValueError) as exc_info:
            MimeType.from_file_type("unknown")

        error_message = str(exc_info.value)
        assert "Known types:" in error_message
        assert "pdf" in error_message
        assert "csv" in error_message

    def test_from_string_error_message_includes_supported_types(self):
        """Test that from_string error message includes supported types"""
        with pytest.raises(ValueError) as exc_info:
            MimeType.from_string("application/unknown")

        error_message = str(exc_info.value)
        assert "Supported types:" in error_message
        assert "application/pdf" in error_message

    def test_get_mime_type_for_extension_error_message_includes_supported_extensions(
        self,
    ):
        """Test that get_mime_type_for_extension error message includes supported extensions"""
        with pytest.raises(ValueError) as exc_info:
            MimeType.get_mime_type_for_extension(".unknown")

        error_message = str(exc_info.value)
        assert "Supported extensions:" in error_message
        assert ".pdf" in error_message


# Made with Bob
