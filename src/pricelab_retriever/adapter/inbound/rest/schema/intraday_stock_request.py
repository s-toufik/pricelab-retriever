from pydantic import BaseModel


class IntradayStockRequest(BaseModel):
    symbol: str
    interval: str
