from pydantic import BaseModel


class CandleSchema(BaseModel):
    source: str
    symbol: str
    timestamp: str
    open: float
    high: float
    low: float
    close: float
    volume: float
