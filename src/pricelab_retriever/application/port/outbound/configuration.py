from abc import ABC, abstractmethod

from pricelab_retriever.domain.model.external_api.api_configuration import ApiConfiguration


class BaseConfiguration(ABC):

    @abstractmethod
    def load(self) -> ApiConfiguration:
        pass