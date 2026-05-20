"""
Unit tests for Event model
"""

from datetime import date, timedelta
import pytest
from pydantic import ValidationError

from app.models.event import Event
from app.enums.event_status import EventStatus


class TestEvent:
    """
    Test Suite for Event model
    """

    @pytest.fixture
    def sample_event_data(self):
        """Fixture providing sample event data"""
        return {
            "title": "Test Event",
            "start_time": date.today(),
            "status": EventStatus.STARTED,
        }

    @pytest.fixture
    def event(self, sample_event_data):
        """Fixture providing an Event instance"""
        return Event(**sample_event_data)

    def test_event_creation_with_required_fields(self):
        """Test creating an Event with required fields"""
        event = Event(
            title="Test Event",
            start_time=date.today(),
            status=EventStatus.STARTED,
        )
        assert event.title == "Test Event"
        assert event.start_time == date.today()
        assert event.finish_time is None
        assert event.status == EventStatus.STARTED

    def test_event_creation_with_different_status(self):
        """Test creating an Event with different status"""
        event = Event(
            title="Conference",
            start_time=date(2024, 1, 15),
            status=EventStatus.SUCCESS,
        )
        assert event.title == "Conference"
        assert event.start_time == date(2024, 1, 15)
        assert event.finish_time is None
        assert event.status == EventStatus.SUCCESS

    def test_event_creation_missing_title_raises_error(self):
        """Test that creating Event without title raises TypeError"""
        with pytest.raises(TypeError):
            Event(  # type: ignore
                start_time=date.today(),
                status=EventStatus.STARTED,
            )

    def test_event_creation_missing_start_time_raises_error(self):
        """Test that creating Event without start_time raises TypeError"""
        with pytest.raises(TypeError):
            Event(  # type: ignore
                title="Test",
                status=EventStatus.STARTED,
            )

    def test_event_creation_missing_status_raises_error(self):
        """Test that creating Event without status raises TypeError"""
        with pytest.raises(TypeError):
            Event(  # type: ignore
                title="Test",
                start_time=date.today(),
            )

    def test_event_creation_with_invalid_status_raises_error(self):
        """Test that creating Event with invalid status raises ValidationError"""
        with pytest.raises(ValidationError):
            Event(
                title="Test",
                start_time=date.today(),
                status="InvalidStatus",  # type: ignore
            )

    def test_get_title(self, event):
        """Test getTitle method returns correct title"""
        assert event.getTitle() == "Test Event"

    def test_set_title_with_valid_string(self, event):
        """Test setTitle method with valid string"""
        event.setTitle("New Title")
        assert event.title == "New Title"
        assert event.getTitle() == "New Title"

    def test_set_title_with_empty_string_does_not_change(self, event):
        """Test setTitle with empty string does not change title"""
        original_title = event.title
        event.setTitle("")
        assert event.title == original_title

    def test_set_title_with_whitespace_only_changes_title(self, event):
        """Test setTitle with whitespace-only string changes title (len > 0)"""
        event.setTitle("   ")
        # The setTitle method only checks if len(title) > 0, not if it's whitespace
        assert event.title == "   "

    def test_get_start_time(self, event):
        """Test getStartTime method returns correct start time"""
        assert event.getStartTime() == date.today()

    def test_set_start_time(self, event):
        """Test setStartTime method sets to today's date"""
        future_date = date.today() + timedelta(days=10)
        event.start_time = future_date

        event.setStartTime()
        assert event.start_time == date.today()
        assert event.getStartTime() == date.today()

    def test_get_finish_time_when_none(self, event):
        """Test getFinishTime method returns None when not set"""
        assert event.getFinishTime() is None

    def test_get_finish_time_after_setting(self, event):
        """Test getFinishTime method returns correct finish time after setting"""
        event.setFinishTime()
        assert event.getFinishTime() == date.today()

    def test_set_finish_time(self, event):
        """Test setFinishTime method sets to today's date"""
        assert event.finish_time is None
        event.setFinishTime()
        assert event.finish_time == date.today()
        assert event.getFinishTime() == date.today()

    def test_set_finish_time_overwrites_existing(self, event):
        """Test setFinishTime overwrites existing finish_time"""
        future_date = date.today() + timedelta(days=10)
        event.finish_time = future_date
        assert event.finish_time == future_date

        event.setFinishTime()
        assert event.finish_time == date.today()

    def test_get_status(self, event):
        """Test getStatus method returns correct status"""
        assert event.getStatus() == EventStatus.STARTED

    def test_set_status_with_valid_status(self, event):
        """Test setStatus method with valid EventStatus"""
        event.setStatus(EventStatus.SUCCESS)
        assert event.status == EventStatus.SUCCESS
        assert event.getStatus() == EventStatus.SUCCESS

    def test_set_status_with_different_valid_statuses(self, event):
        """Test setStatus with all valid EventStatus values"""
        for status in EventStatus:
            event.setStatus(status)
            assert event.status == status
            assert event.getStatus() == status

    def test_set_status_with_default_value(self, event):
        """Test setStatus without parameter uses default STARTED"""
        event.status = EventStatus.SUCCESS
        event.setStatus()
        assert event.status == EventStatus.STARTED

    def test_set_status_with_invalid_status_does_not_change(self, event):
        """Test setStatus with invalid status does not change status"""
        original_status = event.status
        # This will fail the isValid check
        event.setStatus("InvalidStatus")  # type: ignore
        assert event.status == original_status

    def test_event_is_pydantic_model(self, event):
        """Test that Event is a Pydantic BaseModel"""
        from pydantic import BaseModel

        assert isinstance(event, BaseModel)

    def test_event_model_dump(self, event):
        """Test that Event can be dumped to dict"""
        event_dict = event.model_dump()
        assert isinstance(event_dict, dict)
        assert "title" in event_dict
        assert "start_time" in event_dict
        assert "finish_time" in event_dict
        assert "status" in event_dict

    def test_event_model_dump_json(self, event):
        """Test that Event can be dumped to JSON"""
        event_json = event.model_dump_json()
        assert isinstance(event_json, str)
        assert "Test Event" in event_json

    def test_event_with_past_start_date(self):
        """Test creating Event with past start date"""
        past_date = date.today() - timedelta(days=30)
        event = Event(
            title="Past Event",
            start_time=past_date,
            status=EventStatus.SUCCESS,
        )
        assert event.start_time == past_date
        assert event.finish_time is None

        # Set finish time after creation
        event.setFinishTime()
        assert event.finish_time == date.today()

    def test_event_with_future_start_date(self):
        """Test creating Event with future start date"""
        future_date = date.today() + timedelta(days=30)
        event = Event(
            title="Future Event",
            start_time=future_date,
            status=EventStatus.STARTED,
        )
        assert event.start_time == future_date
        assert event.finish_time is None

    def test_event_title_can_be_long_string(self):
        """Test Event with very long title"""
        long_title = "A" * 1000
        event = Event(
            title=long_title,
            start_time=date.today(),
            status=EventStatus.STARTED,
        )
        assert event.title == long_title
        assert len(event.getTitle()) == 1000

    def test_event_title_with_special_characters(self):
        """Test Event title with special characters"""
        special_title = "Event: Test & Demo (2024) - #1 @Location!"
        event = Event(
            title=special_title,
            start_time=date.today(),
            status=EventStatus.STARTED,
        )
        assert event.title == special_title

    def test_event_title_with_unicode_characters(self):
        """Test Event title with unicode characters"""
        unicode_title = "Événement 测试 イベント 🎉"
        event = Event(
            title=unicode_title,
            start_time=date.today(),
            status=EventStatus.STARTED,
        )
        assert event.title == unicode_title

    def test_event_equality_with_same_data(self, sample_event_data):
        """Test that two Events with same data are equal"""
        event1 = Event(**sample_event_data)
        event2 = Event(**sample_event_data)
        assert event1 == event2

    def test_event_inequality_with_different_title(self, sample_event_data):
        """Test that Events with different titles are not equal"""
        event1 = Event(**sample_event_data)
        data2 = sample_event_data.copy()
        data2["title"] = "Different Title"
        event2 = Event(**data2)
        assert event1 != event2

    def test_event_inequality_with_different_status(self, sample_event_data):
        """Test that Events with different statuses are not equal"""
        event1 = Event(**sample_event_data)
        data2 = sample_event_data.copy()
        data2["status"] = EventStatus.SUCCESS
        event2 = Event(**data2)
        assert event1 != event2

    def test_event_inequality_with_different_finish_time(self):
        """Test that Events with different finish_times are not equal"""
        event1 = Event(
            title="Test",
            start_time=date.today(),
            status=EventStatus.STARTED,
        )
        event2 = Event(
            title="Test",
            start_time=date.today(),
            status=EventStatus.STARTED,
        )
        event2.setFinishTime()
        assert event1 != event2

    def test_event_model_copy(self, event):
        """Test that Event can be copied"""
        event_copy = event.model_copy()
        assert event_copy == event
        assert event_copy is not event

    def test_event_model_copy_with_update(self, event):
        """Test that Event can be copied with updates"""
        event_copy = event.model_copy(update={"title": "Updated Title"})
        assert event_copy.title == "Updated Title"
        assert event.title == "Test Event"

    def test_set_title_multiple_times(self, event):
        """Test setting title multiple times"""
        event.setTitle("Title 1")
        assert event.title == "Title 1"

        event.setTitle("Title 2")
        assert event.title == "Title 2"

        event.setTitle("Title 3")
        assert event.title == "Title 3"

    def test_set_status_multiple_times(self, event):
        """Test setting status multiple times"""
        event.setStatus(EventStatus.STARTED)
        assert event.status == EventStatus.STARTED

        event.setStatus(EventStatus.SUCCESS)
        assert event.status == EventStatus.SUCCESS

        event.setStatus(EventStatus.FAILURE)
        assert event.status == EventStatus.FAILURE

    def test_event_workflow_started_to_finished(self):
        """Test typical event workflow from start to finish"""
        # Create event
        event = Event(
            title="Project Meeting",
            start_time=date.today(),
            status=EventStatus.STARTED,
        )
        assert event.finish_time is None

        # Complete event
        event.setFinishTime()
        event.setStatus(EventStatus.SUCCESS)

        assert event.finish_time == date.today()
        assert event.status == EventStatus.SUCCESS

    def test_event_can_manually_set_finish_time_via_attribute(self, event):
        """Test that finish_time can be manually set via direct attribute access"""
        custom_date = date.today() + timedelta(days=5)
        event.finish_time = custom_date
        assert event.getFinishTime() == custom_date

    def test_event_finish_time_initially_none(self):
        """Test that newly created Event has finish_time as None"""
        event = Event(
            title="New Event",
            start_time=date.today(),
            status=EventStatus.STARTED,
        )
        assert event.finish_time is None
        assert event.getFinishTime() is None

    def test_multiple_events_independent(self):
        """Test that multiple Event instances are independent"""
        event1 = Event(
            title="Event 1",
            start_time=date.today(),
            status=EventStatus.STARTED,
        )
        event2 = Event(
            title="Event 2",
            start_time=date.today(),
            status=EventStatus.SUCCESS,
        )

        event1.setFinishTime()

        assert event1.finish_time is not None
        assert event2.finish_time is None
        assert event1.status == EventStatus.STARTED
        assert event2.status == EventStatus.SUCCESS


# Made with Bob
