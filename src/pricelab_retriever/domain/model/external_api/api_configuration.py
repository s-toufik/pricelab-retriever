from typing import List, Optional, Dict, Any
from dataclasses import dataclass

from pricelab_retriever.domain.model.authentication.authentication import Auth

@dataclass(slots=True)
class ApiConfiguration:
    source: str
    base_url: str
    timeout: int
    retry: int
    endpoints: List[Endpoint]
    auth: Auth | None = None

@dataclass(slots=True)
class Endpoint:
    name: str
    path: str
    method: str
    params: Optional[Dict[str, Any]] = None
