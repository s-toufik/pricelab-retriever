import enum
from typing import Dict
from dataclasses import dataclass
from pricelab_retriever.domain.model.data_provider.base import BaseProvider
from pricelab_retriever.domain.model.data_use_case.use_case import UseCase

class DatabaseType(enum.Enum):
    in_memory = "in_memory"
    in_disk = "in_disk"

@dataclass(frozen=True, slots=True)
class AppConfiguration:
    run: str
    primary_database_type: DatabaseType
    secondary_database_type: DatabaseType
    data_providers: Dict[str, BaseProvider]
    data_use_cases: Dict[str, UseCase]