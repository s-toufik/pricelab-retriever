from typing import Sequence

from pricelab_core.domain.model.candles.candle import Candle
from pricelab_core.infrastructure.http.context.request_context import request_id_ctx

from pricelab_retriever.adapter.inbound.rest.mapper.schema_mapper import SchemaMapper
from pricelab_retriever.adapter.inbound.rest.schema.candle_schema import CandleSchema
from pricelab_retriever.adapter.inbound.rest.schema.intraday_request import IntradayRequest
from pricelab_retriever.adapter.inbound.rest.schema.intraday_response import IntradayResponse
from pricelab_retriever.application.port.inbound.get_intraday_stock import GetIntradayStock
from pricelab_core.bootstrap.dependency_injection.logging import logger


class IntradayStockController:
    def __init__(self, use_case: GetIntradayStock, mapper: SchemaMapper):
        self._use_case = use_case
        self._mapper = mapper

    async def get_intraday_stock(self, request: IntradayRequest) -> IntradayResponse:
        request_id = request_id_ctx.get() or "N/A"
        logger.info(f"[{request_id}] request_received")
        candles: Sequence[Candle] = await self._use_case(symbol=request.symbol, interval=request.interval)
        candles_schema: Sequence[CandleSchema] = tuple(self._mapper.map(candles))
        return IntradayResponse(request_id=request_id, payload=candles_schema)
