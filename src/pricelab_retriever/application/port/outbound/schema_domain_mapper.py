from abc import ABC, abstractmethod
from typing import Dict, Any

from pricelab_retriever.domain.model.app.app_configuration import AppConfiguration


class BaseMapperDomainSchema(ABC):
    @abstractmethod
    def map_to_domain(self, data: Dict[str, Any]) -> AppConfiguration:
        pass