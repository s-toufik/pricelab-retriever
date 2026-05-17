from typing import List

from pydantic import BaseModel


class CandleSeriesResponse(BaseModel):
    request_id: str
    symbol: str
    source: str
    time: List[str]
    open: List[float]
    high: List[float]
    low: List[float]
    close: List[float]
    volumes: List[float]
    typical_price: List[float]
    spread: List[float]
