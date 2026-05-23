from fastapi import APIRouter, Depends

from pricelab_retriever.adapter.inbound.rest.schema.intraday_stock_request import IntradayStockRequest
from pricelab_retriever.adapter.inbound.rest.controller.get_intraday_stock import IntradayStockController
from pricelab_retriever.adapter.inbound.rest.schema.intraday_stock_response import IntradayStockResponse


class IntradayStockRouter:
    PREFIX: str = "/api/v1/stocks"

    def __init__(self, controller: IntradayStockController):
        self._controller = controller
        self._router = APIRouter(prefix=self.PREFIX)
        self._router_registry()

    @property
    def router(self) -> APIRouter:
        return self._router

    def _router_registry(self):
        self._router.add_api_route("/intraday", self._get_intraday_stock, methods=["GET"])

    async def _get_intraday_stock(self, request: IntradayStockRequest = Depends()) -> IntradayStockResponse:
        return await self._controller.get_intraday_stock(request)
