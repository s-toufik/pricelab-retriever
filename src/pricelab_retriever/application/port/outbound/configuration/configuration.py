from typing import Protocol

from pricelab_retriever.domain.model.app.app_configuration import AppConfiguration


class Configuration(Protocol):

    def load(self) -> AppConfiguration: ...

    def reload(self) -> AppConfiguration: ...