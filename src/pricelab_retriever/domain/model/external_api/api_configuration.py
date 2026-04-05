from typing import List, Optional, Dict, Any
from dataclasses import dataclass

from pricelab_retriever.domain.model.authentication.authentication import Auth

@dataclass(frozen=True, slots=True)
class ApiConfiguration:
    source: str
    base_url: str
    timeout: int
    retry: int
    auth: Auth
    endpoint: List[Endpoint]

@dataclass
class Endpoint:
    name: str
    path: str
    method: str
    params: Optional[Dict[str, Any]] = None
