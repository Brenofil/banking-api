"""
Unit tests for DocumentProcessingResponse model
"""

import pytest
from pydantic import ValidationError

from app.models.documents.document import DocumentProcessingResponse


class TestDocumentProcessingResponse:
    """
    Test Suite for DocumentProcessingResponse model
    """

    @pytest.fixture
    def sample_response_data(self):
        """Fixture providing sample response data"""
        return {
            "filename": "test_document.pdf",
            "size_bytes": 1024,
            "content_type": "application/pdf",
            "status": "success",
            "message": "Document processed successfully",
        }

    @pytest.fixture
    def response(self, sample_response_data):
        """Fixture providing a DocumentProcessingResponse instance"""
        return DocumentProcessingResponse(**sample_response_data)

    def test_response_creation_with_all_fields(self, sample_response_data):
        """Test creating response with all fields"""
        response = DocumentProcessingResponse(**sample_response_data)
        assert response.filename == "test_document.pdf"
        assert response.size_bytes == 1024
        assert response.content_type == "application/pdf"
        assert response.status == "success"
        assert response.message == "Document processed successfully"

    def test_response_creation_without_content_type(self):
        """Test creating response without optional content_type"""
        response = DocumentProcessingResponse(
            filename="test.txt",
            size_bytes=512,
            content_type=None,
            status="success",
            message="Processed",
        )
        assert response.filename == "test.txt"
        assert response.size_bytes == 512
        assert response.content_type is None
        assert response.status == "success"
        assert response.message == "Processed"

    def test_response_creation_missing_filename_raises_error(self):
        """Test that creating response without filename raises ValidationError"""
        with pytest.raises(ValidationError):
            DocumentProcessingResponse(  # type: ignore
                size_bytes=1024,
                content_type="application/pdf",
                status="success",
                message="Test",
            )

    def test_response_creation_missing_size_bytes_raises_error(self):
        """Test that creating response without size_bytes raises ValidationError"""
        with pytest.raises(ValidationError):
            DocumentProcessingResponse(  # type: ignore
                filename="test.pdf",
                content_type="application/pdf",
                status="success",
                message="Test",
            )

    def test_response_creation_missing_status_raises_error(self):
        """Test that creating response without status raises ValidationError"""
        with pytest.raises(ValidationError):
            DocumentProcessingResponse(  # type: ignore
                filename="test.pdf",
                size_bytes=1024,
                content_type="application/pdf",
                message="Test",
            )

    def test_response_creation_missing_message_raises_error(self):
        """Test that creating response without message raises ValidationError"""
        with pytest.raises(ValidationError):
            DocumentProcessingResponse(  # type: ignore
                filename="test.pdf",
                size_bytes=1024,
                content_type="application/pdf",
                status="success",
            )

    def test_response_with_zero_size_bytes(self):
        """Test response with zero size_bytes"""
        response = DocumentProcessingResponse(
            filename="empty.txt",
            size_bytes=0,
            content_type="text/plain",
            status="success",
            message="Empty file processed",
        )
        assert response.size_bytes == 0

    def test_response_with_large_size_bytes(self):
        """Test response with large size_bytes"""
        large_size = 1024 * 1024 * 100  # 100 MB
        response = DocumentProcessingResponse(
            filename="large_file.pdf",
            size_bytes=large_size,
            content_type="application/pdf",
            status="success",
            message="Large file processed",
        )
        assert response.size_bytes == large_size

    def test_response_with_different_content_types(self):
        """Test response with various content types"""
        content_types = [
            "application/pdf",
            "text/csv",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "application/json",
            "text/plain",
        ]

        for content_type in content_types:
            response = DocumentProcessingResponse(
                filename=f"test.{content_type.split('/')[-1]}",
                size_bytes=1024,
                content_type=content_type,
                status="success",
                message="Processed",
            )
            assert response.content_type == content_type

    def test_response_with_different_statuses(self):
        """Test response with various status values"""
        statuses = ["success", "failed", "processing", "pending", "error"]

        for status in statuses:
            response = DocumentProcessingResponse(
                filename="test.pdf",
                size_bytes=1024,
                content_type="application/pdf",
                status=status,
                message=f"Status: {status}",
            )
            assert response.status == status

    def test_response_with_long_filename(self):
        """Test response with very long filename"""
        long_filename = "a" * 500 + ".pdf"
        response = DocumentProcessingResponse(
            filename=long_filename,
            size_bytes=1024,
            content_type="application/pdf",
            status="success",
            message="Processed",
        )
        assert response.filename == long_filename
        assert len(response.filename) == 504

    def test_response_with_special_characters_in_filename(self):
        """Test response with special characters in filename"""
        special_filename = "test_file-2024 (copy) #1.pdf"
        response = DocumentProcessingResponse(
            filename=special_filename,
            size_bytes=1024,
            content_type="application/pdf",
            status="success",
            message="Processed",
        )
        assert response.filename == special_filename

    def test_response_with_unicode_in_filename(self):
        """Test response with unicode characters in filename"""
        unicode_filename = "文档_документ_文書.pdf"
        response = DocumentProcessingResponse(
            filename=unicode_filename,
            size_bytes=1024,
            content_type="application/pdf",
            status="success",
            message="Processed",
        )
        assert response.filename == unicode_filename

    def test_response_with_long_message(self):
        """Test response with very long message"""
        long_message = "Error: " + "x" * 1000
        response = DocumentProcessingResponse(
            filename="test.pdf",
            size_bytes=1024,
            content_type="application/pdf",
            status="error",
            message=long_message,
        )
        assert response.message == long_message
        assert len(response.message) == 1007

    def test_response_with_multiline_message(self):
        """Test response with multiline message"""
        multiline_message = "Line 1\nLine 2\nLine 3"
        response = DocumentProcessingResponse(
            filename="test.pdf",
            size_bytes=1024,
            content_type="application/pdf",
            status="success",
            message=multiline_message,
        )
        assert response.message == multiline_message
        assert "\n" in response.message

    def test_response_is_pydantic_model(self, response):
        """Test that DocumentProcessingResponse is a Pydantic BaseModel"""
        from pydantic import BaseModel

        assert isinstance(response, BaseModel)

    def test_response_model_dump(self, response):
        """Test that response can be dumped to dict"""
        response_dict = response.model_dump()
        assert isinstance(response_dict, dict)
        assert "filename" in response_dict
        assert "size_bytes" in response_dict
        assert "content_type" in response_dict
        assert "status" in response_dict
        assert "message" in response_dict

    def test_response_model_dump_json(self, response):
        """Test that response can be dumped to JSON"""
        response_json = response.model_dump_json()
        assert isinstance(response_json, str)
        assert "test_document.pdf" in response_json
        assert "1024" in response_json

    def test_response_equality_with_same_data(self, sample_response_data):
        """Test that two responses with same data are equal"""
        response1 = DocumentProcessingResponse(**sample_response_data)
        response2 = DocumentProcessingResponse(**sample_response_data)
        assert response1 == response2

    def test_response_inequality_with_different_filename(self, sample_response_data):
        """Test that responses with different filenames are not equal"""
        response1 = DocumentProcessingResponse(**sample_response_data)
        data2 = sample_response_data.copy()
        data2["filename"] = "different.pdf"
        response2 = DocumentProcessingResponse(**data2)
        assert response1 != response2

    def test_response_inequality_with_different_status(self, sample_response_data):
        """Test that responses with different statuses are not equal"""
        response1 = DocumentProcessingResponse(**sample_response_data)
        data2 = sample_response_data.copy()
        data2["status"] = "failed"
        response2 = DocumentProcessingResponse(**data2)
        assert response1 != response2

    def test_response_model_copy(self, response):
        """Test that response can be copied"""
        response_copy = response.model_copy()
        assert response_copy == response
        assert response_copy is not response

    def test_response_model_copy_with_update(self, response):
        """Test that response can be copied with updates"""
        response_copy = response.model_copy(update={"status": "failed"})
        assert response_copy.status == "failed"
        assert response.status == "success"

    def test_response_with_negative_size_bytes(self):
        """Test response with negative size_bytes (Pydantic allows it)"""
        response = DocumentProcessingResponse(
            filename="test.pdf",
            size_bytes=-100,
            content_type="application/pdf",
            status="error",
            message="Invalid size",
        )
        assert response.size_bytes == -100

    def test_response_with_empty_filename(self):
        """Test response with empty filename (Pydantic allows it)"""
        response = DocumentProcessingResponse(
            filename="",
            size_bytes=0,
            content_type="text/plain",
            status="error",
            message="Empty filename",
        )
        assert response.filename == ""

    def test_response_with_empty_message(self):
        """Test response with empty message (Pydantic allows it)"""
        response = DocumentProcessingResponse(
            filename="test.pdf",
            size_bytes=1024,
            content_type="application/pdf",
            status="success",
            message="",
        )
        assert response.message == ""

    def test_response_with_empty_status(self):
        """Test response with empty status (Pydantic allows it)"""
        response = DocumentProcessingResponse(
            filename="test.pdf",
            size_bytes=1024,
            content_type="application/pdf",
            status="",
            message="No status",
        )
        assert response.status == ""

    def test_response_content_type_can_be_none(self):
        """Test that content_type can be set to None"""
        # content_type is Optional but still required in Pydantic v2
        # It must be explicitly set to None
        response = DocumentProcessingResponse(
            filename="test.pdf",
            size_bytes=1024,
            content_type=None,
            status="success",
            message="Processed",
        )
        assert response.content_type is None

    def test_response_with_path_in_filename(self):
        """Test response with path-like filename"""
        path_filename = "/path/to/document.pdf"
        response = DocumentProcessingResponse(
            filename=path_filename,
            size_bytes=1024,
            content_type="application/pdf",
            status="success",
            message="Processed",
        )
        assert response.filename == path_filename

    def test_response_model_fields(self):
        """Test that response has all expected fields"""
        response = DocumentProcessingResponse(
            filename="test.pdf",
            size_bytes=1024,
            content_type="application/pdf",
            status="success",
            message="Processed",
        )

        assert hasattr(response, "filename")
        assert hasattr(response, "size_bytes")
        assert hasattr(response, "content_type")
        assert hasattr(response, "status")
        assert hasattr(response, "message")

    def test_response_with_various_file_extensions(self):
        """Test response with different file extensions"""
        extensions = [".pdf", ".csv", ".xlsx", ".docx", ".txt", ".json", ".xml"]

        for ext in extensions:
            response = DocumentProcessingResponse(
                filename=f"document{ext}",
                size_bytes=1024,
                content_type="application/octet-stream",
                status="success",
                message=f"Processed {ext} file",
            )
            assert response.filename.endswith(ext)


# Made with Bob
