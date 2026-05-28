from datetime import datetime, UTC
from typing import Sequence, Optional

from pydantic import BaseModel

from pricelab_retriever.adapter.inbound.rest.schema.candle_schema import CandleSchema
from pricelab_retriever.adapter.inbound.rest.schema.quote_schema import QuoteSchema


class IntradayResponse(BaseModel):
    timestamp: str = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")
    request_id: str
    payload: Sequence[CandleSchema | QuoteSchema]
    error: Optional[str] = None
