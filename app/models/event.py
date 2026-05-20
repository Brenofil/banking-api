from datetime import date
from pydantic import BaseModel
from app.enums.event_status import EventStatus


class Event(BaseModel):
    """
    Model of a simple Event for the API.

    A simple Event contains:

    - title: a string containing the event title
    - start_time: a date with the start of the event
    - finish_time: a date with the ending of the event
    - status: a EventStatus
    """

    title: str

    start_time: date

    finish_time: date

    status: EventStatus

    def __init__(self) -> None:
        pass

    def getTitle(self) -> str:
        """
        Get the event's title

        Returns:
            str: the title of the event
        """
        return self.title

    def setTitle(self, title: str) -> None:
        """
        Set the event's title
        """
        if title != "" and len(title) > 0:
            self.title = title

    def getStartTime(self) -> date:
        """
        Get the event's start time

        Returns:
            date: the start time of the event
        """
        return self.start_time

    def setStartTime(self) -> None:
        """
        Set the event's start time
        """
        self.start_time = date.today()

    def getFinishTime(self) -> date:
        """
        Get the event's finish time

        Returns:
            date: the finish time of the event
        """
        return self.finish_time

    def setFinishTime(self) -> None:
        """
        Set the event's finish time
        """
        self.finish_time = date.today()

    def getStatus(self) -> EventStatus:
        """
        Get the event's status

        Returns:
            EventStatus: an event status enumerator value
        """
        return self.status

    def setStatus(self, status: EventStatus = EventStatus.STARTED) -> None:
        """
        Set the event's status
        """
        valid_status: bool = EventStatus.isValid(status)

        if valid_status:
            self.status = status
