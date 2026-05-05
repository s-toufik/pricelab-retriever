from pydantic import BaseModel
from typing import Dict

from pricelab_retriever.domain.model.app.app_configuration import DatabaseType
from pricelab_retriever.domain.model.data_provider.base import BaseProvider
from pricelab_retriever.domain.model.data_use_case.use_case import UseCase

class AppConfigurationSchema(BaseModel):
    run: str
    primary_database_type: DatabaseType
    secondary_database_type: DatabaseType
    data_providers: Dict[str, BaseProvider]
    data_use_cases: Dict[str, UseCase]