from dataclasses import dataclass

from pricelab_retriever.domain.model.data_provider.base import BaseProvider
from pricelab_retriever.domain.model.authentication.authentication import TokenAuth, BasicAuth, NoneAuth


@dataclass(frozen=True, slots=True)
class ApiProvider(BaseProvider):
    base_url: str
    timeout: int
    retry: int
    auth: TokenAuth | BasicAuth | NoneAuth