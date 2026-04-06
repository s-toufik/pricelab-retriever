import threading
from typing import Dict, Any

from pricelab_core.adapter.outbound.file_handler.handler import Handler

from pricelab_retriever.adapter.outbound.configuration.schema_domain_mapper import MapperDomainSchema
from pricelab_retriever.application.port.outbound.configuration import BaseConfiguration
from pricelab_retriever.domain.model.app.app_configuration import AppConfiguration


class Configuration(BaseConfiguration):
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
            raw_configuration = self._read_configuration()
            self._cached_config = MapperDomainSchema().map_to_domain(raw_configuration)
        return self._cached_config

    def reload(self) -> AppConfiguration | None:
        with self._lock:
            raw_configuration = self._read_configuration()
        self._cached_config = MapperDomainSchema().map_to_domain(raw_configuration)
        return self._cached_config

    def _read_configuration(self) -> Dict[str, Any]:
        handler = Handler(self._file_path)
        return handler.read()
