from typing import Sequence

from pricelab_core.domain.model.candles.candle import Candle
from pydantic import BaseModel


class IntradayStockResponse(BaseModel):
    request_id: str
    payload: Sequence[Candle]
