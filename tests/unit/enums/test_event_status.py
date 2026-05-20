"""
Unit tests for EventStatus enum
"""

import pytest
from app.enums.event_status import EventStatus


class TestEventStatus:
    """Test suite for EventStatus enum"""

    def test_enum_values_exist(self):
        """Test that all expected enum values exist"""
        assert EventStatus.STARTED == "Started"
        assert EventStatus.SUCCESS == "Success"
        assert EventStatus.FAILURE == "Failure"

    def test_enum_members_count(self):
        """Test that enum has exactly 3 members"""
        assert len(EventStatus.__members__) == 3

    def test_enum_member_names(self):
        """Test that all expected member names exist"""
        member_names = list(EventStatus.__members__.keys())
        assert "STARTED" in member_names
        assert "SUCCESS" in member_names
        assert "FAILURE" in member_names

    def test_enum_is_string_type(self):
        """Test that enum values are strings"""
        assert isinstance(EventStatus.STARTED.value, str)
        assert isinstance(EventStatus.SUCCESS.value, str)
        assert isinstance(EventStatus.FAILURE.value, str)

    def test_enum_comparison(self):
        """Test enum value comparison"""
        assert EventStatus.STARTED == EventStatus.STARTED
        assert EventStatus.STARTED != EventStatus.SUCCESS
        assert EventStatus.SUCCESS != EventStatus.FAILURE

    def test_enum_string_comparison(self):
        """Test enum comparison with string values"""
        assert EventStatus.STARTED == "Started"
        assert EventStatus.SUCCESS == "Success"
        assert EventStatus.FAILURE == "Failure"

    @pytest.mark.parametrize(
        "status,expected",
        [
            (EventStatus.STARTED, "Started"),
            (EventStatus.SUCCESS, "Success"),
            (EventStatus.FAILURE, "Failure"),
        ],
    )
    def test_enum_value_mapping(self, status, expected):
        """Test that enum values map correctly"""
        assert status.value == expected
        # str() returns the enum name format, not the value
        assert str(status) == f"EventStatus.{status.name}"

    def test_enum_iteration(self):
        """Test iterating over enum members"""
        statuses = [status for status in EventStatus]
        assert len(statuses) == 3
        assert EventStatus.STARTED in statuses
        assert EventStatus.SUCCESS in statuses
        assert EventStatus.FAILURE in statuses

    def test_enum_access_by_name(self):
        """Test accessing enum by member name"""
        assert EventStatus["STARTED"] == EventStatus.STARTED
        assert EventStatus["SUCCESS"] == EventStatus.SUCCESS
        assert EventStatus["FAILURE"] == EventStatus.FAILURE

    def test_enum_access_by_value(self):
        """Test accessing enum by value"""
        assert EventStatus("Started") == EventStatus.STARTED
        assert EventStatus("Success") == EventStatus.SUCCESS
        assert EventStatus("Failure") == EventStatus.FAILURE

    def test_enum_invalid_access_raises_error(self):
        """Test that accessing invalid enum raises error"""
        with pytest.raises(ValueError):
            EventStatus("Invalid")

        with pytest.raises(KeyError):
            EventStatus["INVALID"]

    # Tests for isValid method
    def test_is_valid_with_invalid_status(self):
        """Test isValid returns False for invalid status"""
        assert EventStatus.isValid("Invalid") is False
        assert EventStatus.isValid("") is False

    def test_is_valid_case_sensitive(self):
        """Test isValid is case sensitive"""
        assert EventStatus.isValid("started") is False  # lowercase
        assert EventStatus.isValid("STARTED") is False  # uppercase
        assert EventStatus.isValid("Started") is True  # correct case - valid!
        assert EventStatus.isValid("Success") is True  # correct case - valid!
        assert EventStatus.isValid("Failure") is True  # correct case - valid!

    # Additional edge case tests
    def test_enum_in_list(self):
        """Test enum can be used in lists"""
        status_list = [EventStatus.STARTED, EventStatus.SUCCESS]
        assert EventStatus.STARTED in status_list
        assert EventStatus.FAILURE not in status_list

    def test_enum_in_dict(self):
        """Test enum can be used as dict keys"""
        status_dict = {
            EventStatus.STARTED: "Process started",
            EventStatus.SUCCESS: "Process completed",
            EventStatus.FAILURE: "Process failed",
        }
        assert status_dict[EventStatus.STARTED] == "Process started"
        assert len(status_dict) == 3

    def test_enum_json_serialization(self):
        """Test enum value can be serialized"""
        import json

        status = EventStatus.SUCCESS
        # Enum values are strings, so they serialize directly
        assert json.dumps(status.value) == '"Success"'

    @pytest.mark.parametrize(
        "status",
        [
            EventStatus.STARTED,
            EventStatus.SUCCESS,
            EventStatus.FAILURE,
        ],
    )
    def test_enum_hashable(self, status):
        """Test that enum members are hashable"""
        # Should not raise TypeError
        hash(status)
        # Can be used in sets
        status_set = {status}
        assert status in status_set
