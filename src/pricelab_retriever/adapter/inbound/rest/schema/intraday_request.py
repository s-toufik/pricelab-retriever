from typing import Optional

from pydantic import BaseModel


class IntradayRequest(BaseModel):
    symbol: str
    interval: Optional[str] = None
