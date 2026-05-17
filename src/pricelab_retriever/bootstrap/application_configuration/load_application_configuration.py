import os
import dotenv
from pricelab_core.infrastructure.app_configuration.adapter.load_configuration import LoadConfiguration
from pricelab_core.infrastructure.app_configuration.model.configuration import AppConfiguration
from pricelab_core.bootstrap.dependency_injection.common import logger
from pricelab_core.infrastructure.app_configuration.port.configuration import Configuration


def load_application_configuration() -> AppConfiguration:
    dotenv.load_dotenv()
    configuration_file_path = os.getenv("CONFIGURATION_FILE_PATH")

    if not configuration_file_path:
        exception = FileNotFoundError("No configuration file path provided")
        logger.critical(exception.__str__())
        raise exception

    configuration_loader: Configuration = LoadConfiguration(configuration_file_path, logger)
    configuration = configuration_loader.load()
    if not configuration:
        exception = ValueError("No configuration loaded")
        logger.critical(exception.__str__())
        raise ValueError("No configuration loaded")

    return configuration
