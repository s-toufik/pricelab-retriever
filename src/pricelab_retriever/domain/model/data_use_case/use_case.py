from dataclasses import dataclass
from typing import Dict
from pricelab_retriever.domain.model.data_provider.endpoint import Endpoint


@dataclass(frozen=True, slots=True)
class UseCase:
    name: str
    endpoint: Endpoint
    parameters: Dict[str, str]