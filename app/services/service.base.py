from loguru import Logger
from app.interfaces.base_service_interface import BaseServiceInterface
from app.utils.logger import LoggerService


class BaseService(BaseServiceInterface):
    """
    _summary_

    Args:
        BaseServiceInterface (_type_): _description_
    """

    logger: Logger

    def __init__(self, service_name: str = "") -> None:

        if service_name == "":
            self.service_name = "unknow-service"
        else:
            self.service_name = service_name

        self.logger = LoggerService().get_logger(service_name)

    def registerStart(self) -> None:
        self.logger.info("Registering start of event for service %s")
        pass

    def registerSuccess(self) -> None:
        self.logger.success("Registering success of event for service %s")
        pass

    def registerError(self) -> None:
        self.logger.info("Registering error of event for service %s")
        pass
