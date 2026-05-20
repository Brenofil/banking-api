from enum import Enum


class EventStatus(str, Enum):
    """
    All the status available for an Event type class
    """

    STARTED = "Started"
    SUCCESS = "Success"
    FAILURE = "Failure"

    @classmethod
    def isValid(cls, status: str) -> bool:
        """
        _summary_

        Args:
            status (str): a string containing the status to be validated

        Returns:
            bool: True if the status is an existing value for EventStatus enumerator or False otherwise
        """
        for event_status in EventStatus.__members__.items():
            if event_status is status:
                return True

        return False
