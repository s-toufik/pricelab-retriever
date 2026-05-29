from datetime import datetime, UTC
from typing import Sequence, Optional, Union

from pydantic import BaseModel

from pricelab_retriever.adapter.inbound.rest.schema.candle_schema import CandleSchema
from pricelab_retriever.adapter.inbound.rest.schema.quote_schema import QuoteSchema

payload_typing = Union[CandleSchema, QuoteSchema]


class StockResponse(BaseModel):
    timestamp: str = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")
    request_id: str
    payload: Sequence[payload_typing]
    error: Optional[str] = None
