from typing import Optional

from pydantic import BaseModel


class IntradayStockRequest(BaseModel):
    symbol: str
    interval: Optional[str] = None
