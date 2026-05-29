from typing import Optional

from pydantic import BaseModel


class CandleRequest(BaseModel):
    symbol: str
    interval: Optional[str] = None
