"""
Unit Tests for Markdown Utils
"""

import pytest
import pandas as pd
from unittest.mock import Mock
from app.utils.markdown import MarkdownUtils


class TestMarkdownUtils:
    """
    Test Suite for Markdown Utils
    """

    @pytest.fixture
    def markdown_utils(self):
        """Fixture to create MarkdownUtils instance"""
        return MarkdownUtils()

    def test_parse_markdown_tables_single_table(self, markdown_utils):
        """Test parsing a single valid markdown table"""
        markdown_text = """
| Name | Age | City |
|------|-----|------|
| John | 30  | NYC  |
| Jane | 25  | LA   |
"""
        result = markdown_utils._parse_markdown_tables(markdown_text)

        assert len(result) == 1
        assert result[0]["rows"] == 2
        assert result[0]["columns"] == 3
        assert result[0]["data"]["Name"] == {"0": "John", "1": "Jane"}
        assert result[0]["data"]["Age"] == {"0": "30", "1": "25"}
        assert result[0]["data"]["City"] == {"0": "NYC", "1": "LA"}

    def test_parse_markdown_tables_multiple_tables(self, markdown_utils):
        """Test parsing multiple markdown tables"""
        markdown_text = """
| A | B |
|---|---|
| 1 | 2 |

Some text

| X | Y | Z |
|---|---|---|
| a | b | c |
"""
        result = markdown_utils._parse_markdown_tables(markdown_text)

        assert len(result) == 2
        assert result[0]["columns"] == 2
        assert result[1]["columns"] == 3

    def test_parse_markdown_tables_no_tables(self, markdown_utils):
        """Test parsing text with no tables"""
        markdown_text = "Just some regular text without tables"
        result = markdown_utils._parse_markdown_tables(markdown_text)

        assert result == []

    def test_parse_markdown_tables_invalid_table(self, markdown_utils):
        """Test parsing invalid table (less than 3 lines)"""
        # Regex requires at least 3 lines, so this won't match
        markdown_text = """
| Header |
|--------|
"""
        result = markdown_utils._parse_markdown_tables(markdown_text)

        assert result == []

    def test_parse_markdown_tables_no_valid_data_rows(self, markdown_utils):
        """Test parsing table where all data rows are invalid - covers line 57"""
        markdown_text = """
| A | B | C |
|---|---|---|
| 1 | 2 |
| 3 |
"""
        result = markdown_utils._parse_markdown_tables(markdown_text)

        assert result == []

    def test_parse_markdown_tables_mismatched_columns(self, markdown_utils):
        """Test parsing table with mismatched column count in data row"""
        markdown_text = """
| A | B | C |
|---|---|---|
| 1 | 2 | 3 |
| 4 | 5 |
| 6 | 7 | 8 |
"""
        result = markdown_utils._parse_markdown_tables(markdown_text)

        assert len(result) == 1
        assert result[0]["rows"] == 2  # Only rows with matching columns

    def test_parse_markdown_tables_exception_handling(
        self, markdown_utils, monkeypatch
    ):
        """Test exception handling during table parsing"""
        markdown_text = """
| A | B |
|---|---|
| 1 | 2 |
"""
        # Mock the logger to verify warning is called
        mock_logger = Mock()
        monkeypatch.setattr(markdown_utils, "logger", mock_logger)

        # Force an exception by mocking enumerate to raise an error
        original_enumerate = enumerate

        def mock_enumerate(*args, **kwargs):
            raise RuntimeError("Forced error")

        monkeypatch.setattr("builtins.enumerate", mock_enumerate)
        result = markdown_utils._parse_markdown_tables(markdown_text)

        assert result == []
        assert mock_logger.warning.called

    def test_read_pdf_response_single_table(self, markdown_utils):
        """Test converting single table to DataFrame"""
        response_data = {
            "tables": [
                {
                    "data": {
                        "Name": {"0": "John", "1": "Jane"},
                        "Age": {"0": "30", "1": "25"},
                    },
                    "rows": 2,
                    "columns": 2,
                }
            ]
        }

        result = markdown_utils.read_pdf_response_to_dataframes(response_data)

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert list(result.columns) == ["Name", "Age"]

    def test_read_pdf_response_multiple_tables_same_columns(self, markdown_utils):
        """Test converting multiple tables with same columns to single DataFrame"""
        response_data = {
            "tables": [
                {"data": {"Name": {"0": "John"}, "Age": {"0": "30"}}},
                {"data": {"Name": {"0": "Jane"}, "Age": {"0": "25"}}},
            ]
        }

        result = markdown_utils.read_pdf_response_to_dataframes(response_data)

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2

    def test_read_pdf_response_multiple_tables_different_columns(self, markdown_utils):
        """Test converting multiple tables with different columns to list"""
        response_data = {
            "tables": [
                {"data": {"Name": {"0": "John"}, "Age": {"0": "30"}}},
                {"data": {"City": {"0": "NYC"}, "Country": {"0": "USA"}}},
            ]
        }

        result = markdown_utils.read_pdf_response_to_dataframes(response_data)

        assert isinstance(result, list)
        assert len(result) == 2
        assert isinstance(result[0], pd.DataFrame)
        assert isinstance(result[1], pd.DataFrame)

    def test_read_pdf_response_missing_tables_field(self, markdown_utils):
        """Test error handling when 'tables' field is missing"""
        response_data = {"other_field": "value"}

        with pytest.raises(ValueError, match="missing 'tables' field"):
            markdown_utils.read_pdf_response_to_dataframes(response_data)

    def test_read_pdf_response_empty_tables(self, markdown_utils):
        """Test error handling when tables list is empty"""
        response_data = {"tables": []}

        with pytest.raises(ValueError, match="No tables found"):
            markdown_utils.read_pdf_response_to_dataframes(response_data)

    def test_read_pdf_response_table_missing_data(self, markdown_utils):
        """Test handling table without 'data' field"""
        response_data = {
            "tables": [{"index": 0, "rows": 1}, {"data": {"Name": {"0": "John"}}}]
        }

        result = markdown_utils.read_pdf_response_to_dataframes(response_data)

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1

    def test_read_pdf_response_all_tables_invalid(self, markdown_utils):
        """Test error when all tables are invalid"""
        response_data = {"tables": [{"no_data": "field"}, {"also_no_data": "field"}]}

        with pytest.raises(ValueError, match="No valid tables could be converted"):
            markdown_utils.read_pdf_response_to_dataframes(response_data)

    def test_read_pdf_response_generic_exception(self, markdown_utils, monkeypatch):
        """Test generic exception handling"""
        response_data = {"tables": [{"data": {"Name": {"0": "John"}}}]}

        # Force an exception in DataFrame creation
        def mock_dataframe(*args, **kwargs):
            raise RuntimeError("Forced error")

        monkeypatch.setattr(pd, "DataFrame", mock_dataframe)

        with pytest.raises(RuntimeError):
            markdown_utils.read_pdf_response_to_dataframes(response_data)
