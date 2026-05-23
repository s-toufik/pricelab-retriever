from datetime import datetime, UTC
from typing import Sequence, Optional

from pricelab_core.domain.model.candles.candle import Candle
from pydantic import BaseModel


class IntradayStockResponse(BaseModel):
    timestamp: str = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")
    request_id: str
    payload: Sequence[Candle]
    error: Optional[str] = None
