from fastapi import APIRouter, Depends

from pricelab_retriever.adapter.inbound.rest.schema.intraday_request import IntradayRequest
from pricelab_retriever.adapter.inbound.rest.controller.get_intraday_stock import IntradayStockController
from pricelab_retriever.adapter.inbound.rest.schema.intraday_response import IntradayResponse


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
        self._router.add_api_route("/intraday", self._get_intraday_stock, methods=["GET"], response_model=IntradayResponse)

    async def _get_intraday_stock(self, request: IntradayRequest = Depends()) -> IntradayResponse:
        return await self._controller.get_intraday_stock(request)
