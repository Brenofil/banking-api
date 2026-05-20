"""
Unit tests for ProcessorResponse model
"""

from datetime import datetime, timezone
from typing import Any, Dict, List

import pytest
from pydantic import BaseModel, ValidationError

from app.enums.processing_status import ProcessingStatus
from app.models.documents.processor import ProcessorResponse


class TestProcessorResponse:
    """
    Test Suite for ProcessorResponse model
    """

    # ==================== Model Creation Tests ====================

    def test_response_creation_with_required_fields_only(self):
        """Test creating response with only required fields"""
        response = ProcessorResponse(
            status=ProcessingStatus.SUCCESS, processor_type="pdf"
        )

        assert response.status == ProcessingStatus.SUCCESS
        assert response.processor_type == "pdf"
        assert response.data is None
        assert response.metadata is None
        assert response.processing_time_ms is None
        assert response.errors is None
        assert response.warnings is None
        assert response.extracted_text is None
        assert response.page_count is None
        assert response.tables is None
        assert response.images is None
        assert response.confidence_score is None
        assert isinstance(response.processed_at, datetime)

    def test_response_creation_with_all_fields(self):
        """Test creating response with all fields populated"""
        test_datetime = datetime(2024, 1, 1, 12, 0, 0)

        response = ProcessorResponse(
            status=ProcessingStatus.SUCCESS,
            data={"key": "value"},
            metadata={"file_size": 1024},
            processor_type="pdf",
            processing_time_ms=1250.5,
            errors=["error1"],
            warnings=["warning1"],
            extracted_text="Sample text",
            page_count=5,
            tables=[{"rows": 10}],
            images=[{"page": 1}],
            processed_at=test_datetime,
            confidence_score=0.95,
        )

        assert response.status == ProcessingStatus.SUCCESS
        assert response.data == {"key": "value"}
        assert response.metadata == {"file_size": 1024}
        assert response.processor_type == "pdf"
        assert response.processing_time_ms == 1250.5
        assert response.errors == ["error1"]
        assert response.warnings == ["warning1"]
        assert response.extracted_text == "Sample text"
        assert response.page_count == 5
        assert response.tables == [{"rows": 10}]
        assert response.images == [{"page": 1}]
        assert response.processed_at == test_datetime
        assert response.confidence_score == 0.95

    def test_response_creation_missing_status_raises_error(self):
        """Test that missing status raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            ProcessorResponse(processor_type="pdf")  # type: ignore

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("status",) for error in errors)

    def test_response_creation_missing_processor_type_raises_error(self):
        """Test that missing processor_type raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            ProcessorResponse(status=ProcessingStatus.SUCCESS)  # type: ignore

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("processor_type",) for error in errors)

    # ==================== Status Field Tests ====================

    def test_response_with_all_status_values(self):
        """Test response with all ProcessingStatus enum values"""
        statuses = [
            ProcessingStatus.SUCCESS,
            ProcessingStatus.PARTIAL_SUCCESS,
            ProcessingStatus.FAILED,
            ProcessingStatus.VALIDATION_ERROR,
            ProcessingStatus.UNSUPPORTED_FORMAT,
        ]

        for status in statuses:
            response = ProcessorResponse(status=status, processor_type="pdf")
            assert response.status == status

    def test_response_with_invalid_status_raises_error(self):
        """Test that invalid status value raises ValidationError"""
        with pytest.raises(ValidationError):
            ProcessorResponse(
                status="invalid_status", processor_type="pdf"  # type: ignore
            )

    # ==================== Processor Type Tests ====================

    def test_response_with_different_processor_types(self):
        """Test response with various processor types"""
        processor_types = ["pdf", "csv", "xlsx", "docx", "txt"]

        for proc_type in processor_types:
            response = ProcessorResponse(
                status=ProcessingStatus.SUCCESS, processor_type=proc_type
            )
            assert response.processor_type == proc_type

    def test_response_with_empty_processor_type(self):
        """Test response with empty processor_type string"""
        response = ProcessorResponse(status=ProcessingStatus.SUCCESS, processor_type="")
        assert response.processor_type == ""

    # ==================== Data and Metadata Tests ====================

    def test_response_with_complex_data_structure(self):
        """Test response with complex nested data"""
        complex_data = {
            "transactions": [
                {"date": "2024-01-01", "amount": 100.50},
                {"date": "2024-01-02", "amount": 200.75},
            ],
            "summary": {"total": 301.25, "count": 2},
        }

        response = ProcessorResponse(
            status=ProcessingStatus.SUCCESS, processor_type="pdf", data=complex_data
        )

        assert response.data == complex_data
        assert response.data["transactions"][0]["amount"] == 100.50  # type: ignore

    def test_response_with_complex_metadata(self):
        """Test response with complex metadata"""
        metadata = {
            "file_size": 1024,
            "format": "PDF",
            "version": "1.7",
            "author": "Test Author",
            "created": "2024-01-01",
        }

        response = ProcessorResponse(
            status=ProcessingStatus.SUCCESS, processor_type="pdf", metadata=metadata
        )

        assert response.metadata == metadata

    # ==================== Processing Time Tests ====================

    def test_response_with_zero_processing_time(self):
        """Test response with zero processing time"""
        response = ProcessorResponse(
            status=ProcessingStatus.SUCCESS,
            processor_type="pdf",
            processing_time_ms=0.0,
        )
        assert response.processing_time_ms == 0.0

    def test_response_with_large_processing_time(self):
        """Test response with large processing time"""
        response = ProcessorResponse(
            status=ProcessingStatus.SUCCESS,
            processor_type="pdf",
            processing_time_ms=999999.99,
        )
        assert response.processing_time_ms == 999999.99

    def test_response_with_negative_processing_time(self):
        """Test response with negative processing time (should be allowed)"""
        response = ProcessorResponse(
            status=ProcessingStatus.SUCCESS,
            processor_type="pdf",
            processing_time_ms=-100.0,
        )
        assert response.processing_time_ms == -100.0

    # ==================== Errors and Warnings Tests ====================

    def test_response_with_multiple_errors(self):
        """Test response with multiple error messages"""
        errors = [
            "Failed to parse page 1",
            "Invalid data format on page 2",
            "Missing required field",
        ]

        response = ProcessorResponse(
            status=ProcessingStatus.FAILED, processor_type="pdf", errors=errors
        )

        assert response.errors == errors
        assert len(response.errors) == 3  # type: ignore

    def test_response_with_multiple_warnings(self):
        """Test response with multiple warning messages"""
        warnings = [
            "Some formatting may be lost",
            "Image quality reduced",
            "Table structure simplified",
        ]

        response = ProcessorResponse(
            status=ProcessingStatus.PARTIAL_SUCCESS,
            processor_type="pdf",
            warnings=warnings,
        )

        assert response.warnings == warnings
        assert len(response.warnings) == 3  # type: ignore

    def test_response_with_empty_errors_list(self):
        """Test response with empty errors list"""
        response = ProcessorResponse(
            status=ProcessingStatus.SUCCESS, processor_type="pdf", errors=[]
        )
        assert response.errors == []

    def test_response_with_empty_warnings_list(self):
        """Test response with empty warnings list"""
        response = ProcessorResponse(
            status=ProcessingStatus.SUCCESS, processor_type="pdf", warnings=[]
        )
        assert response.warnings == []

    # ==================== Extracted Text Tests ====================

    def test_response_with_long_extracted_text(self):
        """Test response with long extracted text"""
        long_text = "Lorem ipsum " * 1000

        response = ProcessorResponse(
            status=ProcessingStatus.SUCCESS,
            processor_type="pdf",
            extracted_text=long_text,
        )

        assert response.extracted_text == long_text
        assert len(response.extracted_text) > 10000  # type: ignore

    def test_response_with_multiline_extracted_text(self):
        """Test response with multiline extracted text"""
        multiline_text = "Line 1\nLine 2\nLine 3\n"

        response = ProcessorResponse(
            status=ProcessingStatus.SUCCESS,
            processor_type="pdf",
            extracted_text=multiline_text,
        )

        assert response.extracted_text == multiline_text
        assert "\n" in response.extracted_text

    def test_response_with_empty_extracted_text(self):
        """Test response with empty extracted text"""
        response = ProcessorResponse(
            status=ProcessingStatus.SUCCESS, processor_type="pdf", extracted_text=""
        )
        assert response.extracted_text == ""

    def test_response_with_unicode_extracted_text(self):
        """Test response with unicode characters in extracted text"""
        unicode_text = "Hello 世界 🌍 Привет"

        response = ProcessorResponse(
            status=ProcessingStatus.SUCCESS,
            processor_type="pdf",
            extracted_text=unicode_text,
        )

        assert response.extracted_text == unicode_text

    # ==================== Page Count Tests ====================

    def test_response_with_zero_page_count(self):
        """Test response with zero page count"""
        response = ProcessorResponse(
            status=ProcessingStatus.SUCCESS, processor_type="pdf", page_count=0
        )
        assert response.page_count == 0

    def test_response_with_large_page_count(self):
        """Test response with large page count"""
        response = ProcessorResponse(
            status=ProcessingStatus.SUCCESS, processor_type="pdf", page_count=10000
        )
        assert response.page_count == 10000

    def test_response_with_negative_page_count(self):
        """Test response with negative page count (should be allowed)"""
        response = ProcessorResponse(
            status=ProcessingStatus.SUCCESS, processor_type="pdf", page_count=-1
        )
        assert response.page_count == -1

    # ==================== Tables Tests ====================

    def test_response_with_multiple_tables(self):
        """Test response with multiple tables"""
        tables = [
            {"rows": 10, "columns": 5, "page": 1},
            {"rows": 20, "columns": 3, "page": 2},
            {"rows": 15, "columns": 7, "page": 3},
        ]

        response = ProcessorResponse(
            status=ProcessingStatus.SUCCESS, processor_type="pdf", tables=tables
        )

        assert response.tables == tables
        assert len(response.tables) == 3  # type: ignore

    def test_response_with_empty_tables_list(self):
        """Test response with empty tables list"""
        response = ProcessorResponse(
            status=ProcessingStatus.SUCCESS, processor_type="pdf", tables=[]
        )
        assert response.tables == []

    # ==================== Images Tests ====================

    def test_response_with_multiple_images(self):
        """Test response with multiple images"""
        images = [
            {"page": 1, "format": "jpeg", "size": 1024},
            {"page": 2, "format": "png", "size": 2048},
            {"page": 3, "format": "gif", "size": 512},
        ]

        response = ProcessorResponse(
            status=ProcessingStatus.SUCCESS, processor_type="pdf", images=images
        )

        assert response.images == images
        assert len(response.images) == 3  # type: ignore

    def test_response_with_empty_images_list(self):
        """Test response with empty images list"""
        response = ProcessorResponse(
            status=ProcessingStatus.SUCCESS, processor_type="pdf", images=[]
        )
        assert response.images == []

    # ==================== Processed At Tests ====================

    def test_response_processed_at_default_factory(self):
        """Test that processed_at is automatically set to current time"""
        response = ProcessorResponse(
            status=ProcessingStatus.SUCCESS, processor_type="pdf"
        )

        assert isinstance(response.processed_at, datetime)
        # Check it's recent (within last minute)
        time_diff = datetime.now(timezone.utc) - response.processed_at
        assert time_diff.total_seconds() < 60

    def test_response_with_custom_processed_at(self):
        """Test response with custom processed_at timestamp"""
        custom_time = datetime(2024, 6, 15, 10, 30, 0)

        response = ProcessorResponse(
            status=ProcessingStatus.SUCCESS,
            processor_type="pdf",
            processed_at=custom_time,
        )

        assert response.processed_at == custom_time

    # ==================== Confidence Score Tests ====================

    def test_response_with_valid_confidence_scores(self):
        """Test response with various valid confidence scores"""
        valid_scores = [0.0, 0.25, 0.5, 0.75, 0.95, 1.0]

        for score in valid_scores:
            response = ProcessorResponse(
                status=ProcessingStatus.SUCCESS,
                processor_type="pdf",
                confidence_score=score,
            )
            assert response.confidence_score == score

    def test_response_with_confidence_score_below_zero_raises_error(self):
        """Test that confidence score below 0.0 raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            ProcessorResponse(
                status=ProcessingStatus.SUCCESS,
                processor_type="pdf",
                confidence_score=-0.1,
            )

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("confidence_score",) for error in errors)

    def test_response_with_confidence_score_above_one_raises_error(self):
        """Test that confidence score above 1.0 raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            ProcessorResponse(
                status=ProcessingStatus.SUCCESS,
                processor_type="pdf",
                confidence_score=1.1,
            )

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("confidence_score",) for error in errors)

    # ==================== Pydantic Model Features Tests ====================

    def test_response_is_pydantic_model(self):
        """Test that ProcessorResponse is a Pydantic BaseModel"""
        response = ProcessorResponse(
            status=ProcessingStatus.SUCCESS, processor_type="pdf"
        )
        assert isinstance(response, BaseModel)

    def test_response_model_dump(self):
        """Test model_dump() converts response to dictionary"""
        response = ProcessorResponse(
            status=ProcessingStatus.SUCCESS, processor_type="pdf", data={"key": "value"}
        )

        result = response.model_dump()

        assert isinstance(result, dict)
        assert result["status"] == ProcessingStatus.SUCCESS
        assert result["processor_type"] == "pdf"
        assert result["data"] == {"key": "value"}

    def test_response_model_dump_json(self):
        """Test model_dump_json() converts response to JSON string"""
        response = ProcessorResponse(
            status=ProcessingStatus.SUCCESS, processor_type="pdf"
        )

        result = response.model_dump_json()

        assert isinstance(result, str)
        assert "success" in result
        assert "pdf" in result

    def test_response_model_copy(self):
        """Test model_copy() creates a copy of the response"""
        original = ProcessorResponse(
            status=ProcessingStatus.SUCCESS, processor_type="pdf", page_count=5
        )

        copy = original.model_copy()

        assert copy.status == original.status
        assert copy.processor_type == original.processor_type
        assert copy.page_count == original.page_count
        assert copy is not original

    def test_response_model_copy_with_update(self):
        """Test model_copy() with update parameter"""
        original = ProcessorResponse(
            status=ProcessingStatus.SUCCESS, processor_type="pdf", page_count=5
        )

        copy = original.model_copy(update={"page_count": 10})

        assert copy.status == original.status
        assert copy.processor_type == original.processor_type
        assert copy.page_count == 10
        assert original.page_count == 5

    # ==================== Equality Tests ====================

    def test_response_equality_with_same_data(self):
        """Test that two responses with same data are equal"""
        response1 = ProcessorResponse(
            status=ProcessingStatus.SUCCESS, processor_type="pdf", page_count=5
        )

        response2 = ProcessorResponse(
            status=ProcessingStatus.SUCCESS, processor_type="pdf", page_count=5
        )

        # Note: processed_at will be different, so we need to set it
        response2.processed_at = response1.processed_at

        assert response1 == response2

    def test_response_inequality_with_different_status(self):
        """Test that responses with different status are not equal"""
        response1 = ProcessorResponse(
            status=ProcessingStatus.SUCCESS, processor_type="pdf"
        )

        response2 = ProcessorResponse(
            status=ProcessingStatus.FAILED, processor_type="pdf"
        )

        assert response1 != response2

    def test_response_inequality_with_different_processor_type(self):
        """Test that responses with different processor_type are not equal"""
        response1 = ProcessorResponse(
            status=ProcessingStatus.SUCCESS, processor_type="pdf"
        )

        response2 = ProcessorResponse(
            status=ProcessingStatus.SUCCESS, processor_type="csv"
        )

        assert response1 != response2

    # ==================== Config and Schema Tests ====================

    def test_response_has_model_config(self):
        """Test that ProcessorResponse has model_config"""
        assert hasattr(ProcessorResponse, "model_config")

    def test_response_model_config_has_json_schema_extra(self):
        """Test that model_config has json_schema_extra with example"""
        assert "json_schema_extra" in ProcessorResponse.model_config
        schema_extra = ProcessorResponse.model_config["json_schema_extra"]  # type: ignore
        assert isinstance(schema_extra, dict)
        assert "example" in schema_extra

    def test_response_json_schema_extra_example_structure(self):
        """Test that json_schema_extra example has correct structure"""
        example = ProcessorResponse.model_config["json_schema_extra"]["example"]  # type: ignore

        assert "status" in example  # type: ignore
        assert "processor_type" in example  # type: ignore
        assert "data" in example  # type: ignore
        assert "metadata" in example  # type: ignore
        assert example["status"] == "success"  # type: ignore
        assert example["processor_type"] == "pdf"  # type: ignore

    def test_response_model_fields(self):
        """Test that all expected fields are present in the model"""
        response = ProcessorResponse(
            status=ProcessingStatus.SUCCESS, processor_type="pdf"
        )

        fields = response.model_fields
        expected_fields = [
            "status",
            "data",
            "metadata",
            "processor_type",
            "processing_time_ms",
            "errors",
            "warnings",
            "extracted_text",
            "page_count",
            "tables",
            "images",
            "processed_at",
            "confidence_score",
        ]

        for field in expected_fields:
            assert field in fields

    # ==================== Complex Scenario Tests ====================

    def test_response_success_scenario(self):
        """Test complete success scenario with all relevant fields"""
        response = ProcessorResponse(
            status=ProcessingStatus.SUCCESS,
            processor_type="pdf",
            data={"transactions": [{"amount": 100}]},
            metadata={"file_size": 1024},
            processing_time_ms=1250.5,
            extracted_text="Sample text",
            page_count=5,
            tables=[{"rows": 10}],
            images=[{"page": 1}],
            confidence_score=0.95,
        )

        assert response.status == ProcessingStatus.SUCCESS
        assert response.errors is None
        assert response.warnings is None
        assert response.confidence_score == 0.95

    def test_response_failure_scenario(self):
        """Test complete failure scenario with errors"""
        response = ProcessorResponse(
            status=ProcessingStatus.FAILED,
            processor_type="pdf",
            errors=["Failed to parse document", "Invalid format"],
            processing_time_ms=500.0,
        )

        assert response.status == ProcessingStatus.FAILED
        assert len(response.errors) == 2  # type: ignore
        assert response.data is None
        assert response.confidence_score is None

    def test_response_partial_success_scenario(self):
        """Test partial success scenario with warnings"""
        response = ProcessorResponse(
            status=ProcessingStatus.PARTIAL_SUCCESS,
            processor_type="pdf",
            data={"partial_data": "value"},
            warnings=["Some data could not be extracted"],
            extracted_text="Partial text",
            page_count=5,
            confidence_score=0.65,
        )

        assert response.status == ProcessingStatus.PARTIAL_SUCCESS
        assert len(response.warnings) == 1  # type: ignore
        assert response.data is not None
        assert response.confidence_score == 0.65


# Made with Bob
