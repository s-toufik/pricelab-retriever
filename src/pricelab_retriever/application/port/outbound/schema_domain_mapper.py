from abc import ABC, abstractmethod

from pricelab_retriever.domain.model.app.app_configuration import AppConfiguration


class SchemaToDomainMapper(ABC):

    @abstractmethod
    def map_to_app_configuration(self, schema: object) -> AppConfiguration:
        pass