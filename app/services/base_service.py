from typing import Optional
from loguru import Logger
from app.interfaces.base_service_interface import BaseServiceInterface
from app.utils.logger import get_logger


class BaseService(BaseServiceInterface):
    """
    _summary_

    Args:
        BaseServiceInterface (_type_): _description_
    """

    logger: Logger

    def __init__(self) -> None:
        self.logger = get_logger()

    # TODO should add event repository actions
    def registerStart(self) -> None:
        self.logger.info("Registering start of event for service")
        pass

    # TODO should add event repository actions
    def registerSuccess(self) -> None:
        self.logger.info("Registering success of event for service")
        pass

    # TODO should add event repository actions
    def registerError(self, error: Exception, context: Optional[dict] = None) -> None:
        if context:
            self.logger.bind(**context).exception(f"Error in service {str(error)}")
        else:
            self.logger.exception(f"Error in service: {str(error)}")
