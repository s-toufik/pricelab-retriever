from fastapi import APIRouter, Depends

from pricelab_retriever.adapter.inbound.rest.schema.stock_request import CandleRequest
from pricelab_retriever.adapter.inbound.rest.controller.stock_candle_controller import StockCandleController
from pricelab_retriever.adapter.inbound.rest.schema.stock_response import StockResponse


class StockCandleRouter:
    PREFIX: str = "/api/v1/stocks"

    def __init__(self, controller: StockCandleController):
        self._controller = controller
        self._router = APIRouter(prefix=self.PREFIX)
        self._router_registry()

    @property
    def router(self) -> APIRouter:
        return self._router

    def _router_registry(self):
        self._router.add_api_route("/candle", self._get_stock_candle, methods=["GET"], response_model=StockResponse)

    async def _get_stock_candle(self, request: CandleRequest = Depends()) -> StockResponse:
        return await self._controller.get_stock_candle(request)
