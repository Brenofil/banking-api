from abc import ABC, abstractmethod


class BaseServiceInterface(ABC):
    """
    _summary_

    Args:
        ABC (_type_): _description_
    """

    @abstractmethod
    def registerStart(self) -> None:
        """
        Method responsible for registering the start of an action within a service.
        """
        pass

    @abstractmethod
    def registerSuccess(self) -> None:
        """
        Method responsible for registering the success of an action within a service.

        It register the success in the logger and set an end to the event.
        """
        pass

    @abstractmethod
    def registerError(self) -> None:
        """
        Method responsible for registering an action error within a service.

        It register the error in the logger, sets an end to the event and throw the appropriate error.
        """
        pass
