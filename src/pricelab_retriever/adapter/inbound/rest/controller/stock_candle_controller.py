from typing import Sequence

from pricelab_core.domain.model.candles.candle import Candle
from pricelab_core.infrastructure.http.context.request_context import request_id_ctx

from pricelab_retriever.adapter.inbound.rest.mapper.schema_mapper import SchemaMapper
from pricelab_retriever.adapter.inbound.rest.schema.candle_schema import CandleSchema
from pricelab_retriever.adapter.inbound.rest.schema.stock_request import CandleRequest
from pricelab_retriever.adapter.inbound.rest.schema.stock_response import StockResponse
from pricelab_retriever.application.port.inbound.stock_candle import StockCandle, StockCandleQuery
from pricelab_core.bootstrap.dependency_injection.logging import logger


class StockCandleController:
    def __init__(self, use_case: StockCandle, mapper: SchemaMapper):
        self._use_case = use_case
        self._mapper = mapper

    async def get_stock_candle(self, request: CandleRequest) -> StockResponse:
        request_id = request_id_ctx.get() or "N/A"
        logger.info(f"[{request_id}] request_received")
        query = StockCandleQuery(symbol=request.symbol, interval=request.interval)
        candles: Sequence[Candle] = await self._use_case(query)
        candles_schema: Sequence[CandleSchema] = tuple(self._mapper.map(candles))
        return StockResponse(request_id=request_id, payload=candles_schema)
