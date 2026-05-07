import threading
from typing import Dict, Any

from pricelab_core.adapter.outbound.file_handler.handler import Handler
from pricelab_core.bootstrap.common import logger

from pricelab_retriever.adapter.outbound.configuration.schema import AppConfigurationSchema, MapperDomainSchema
from pricelab_retriever.domain.model.app.app_configuration import AppConfiguration

TAG: str = "app_configuration"

class LoadConfiguration:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, file_path: str):
        if not hasattr(self, "_file_path"):
            self._file_path = file_path
            self._cached_config: AppConfiguration | None = None

    def load(self) -> AppConfiguration | None:
        if self._cached_config is None:
            try:
                configuration = self._read_and_validate_configuration()
                self._cached_config = MapperDomainSchema().map(configuration)
            except Exception as exception:
                logger.error(exception.__str__())
        return self._cached_config

    def reload(self) -> AppConfiguration | None:
        with self._lock:
            configuration = self._read_and_validate_configuration()
        self._cached_config = MapperDomainSchema().map(configuration)
        return self._cached_config

    def _read_configuration_file(self) -> Dict[str, Any]:
        handler = Handler(self._file_path)
        return handler.read()

    def _read_and_validate_configuration(self) -> AppConfigurationSchema:
        raw_configuration = self._read_configuration_file()
        return AppConfigurationSchema(**raw_configuration[TAG])
