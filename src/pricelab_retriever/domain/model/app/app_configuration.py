from typing import List
from dataclasses import dataclass

from pricelab_retriever.domain.model.external_api.api_configuration import ApiConfiguration


@dataclass(frozen=True, slots=True)
class AppBaseConfiguration:
    run: str
    primary_database_type: str
    secondary_database_type: str

@dataclass(frozen=True, slots=True)
class AppConfiguration:
    base: AppBaseConfiguration
    external_api_registery: List[ApiConfiguration]