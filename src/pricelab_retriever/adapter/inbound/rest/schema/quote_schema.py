from pydantic import BaseModel


class QuoteSchema(BaseModel):
    source: str
    symbol: str
    timestamp: str
    bid: float
    ask: float
    last: float
    volume: float
