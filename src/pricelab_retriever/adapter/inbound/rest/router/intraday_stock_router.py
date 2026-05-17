from fastapi import APIRouter, Depends
from pricelab_core.infrastructure.http.context.request_context import request_id_ctx

from pricelab_retriever.adapter.inbound.rest.schema.intraday_stock_request import IntradayStockRequest
from pricelab_retriever.adapter.inbound.rest.schema.intraday_stock_response import CandleSeriesResponse
from pricelab_retriever.application.port.inbound.get_intraday_stock import GetIntradayStock
from pricelab_core.bootstrap.dependency_injection.common import logger


class IntradayStock:
    PREFIX: str = "/api/v1/stocks"

    def __init__(self, use_case: GetIntradayStock):
        self._use_case = use_case
        self.router = APIRouter(prefix=self.PREFIX)
        self._register_route()

    def _register_route(self):

        self.router.add_api_route("/intraday", self.get_intraday_stock, methods=["GET"])

    async def get_intraday_stock(self, request: IntradayStockRequest = Depends()) -> CandleSeriesResponse:
        request_id = request_id_ctx.get() or "N/A"
        logger.info(f"[{request_id}] request_received")
        candles = await self._use_case(symbol=request.symbol, interval=request.interval)
        return CandleSeriesResponse(request_id=request_id, payload=candles)
