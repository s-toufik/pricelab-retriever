from dataclasses import dataclass
from enum import Enum

from pricelab_retriever.domain.model.data_provider.api import ApiProvider

class HttpMethod(Enum):
    GET = "GET"
    POST = "POST"

@dataclass(slots=True)
class Endpoint:
    name: str
    provider: ApiProvider
    path: str
    method: HttpMethod
