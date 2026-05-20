from fastapi import APIRouter
from pricelab_core.infrastructure.app_configuration.model.configuration import AppConfiguration
from pricelab_core.infrastructure.telemetry.adapter.open_telemetry import OpenTelemetryManager


from pricelab_retriever.adapter.inbound.rest.controller.get_intraday_stock import IntradayStockController
from pricelab_retriever.adapter.outbound.alpha_vantage.adapter import AlphaVantageMarketDataFetcher
from pricelab_retriever.adapter.outbound.alpha_vantage.factory import AlphaVantageClientFactory
from pricelab_retriever.adapter.outbound.alpha_vantage.mapper import Mapper
from pricelab_retriever.application.port.inbound.get_intraday_stock import GetIntradayStock
from pricelab_retriever.application.port.outbound.market_data_fetcher import MarketDataFetcher
from pricelab_retriever.application.use_cases.get_intraday_stock import GetIntradayStockUseCase
from pricelab_retriever.bootstrap.application_configuration.load_application_configuration import (
    load_application_configuration,
)
from pricelab_retriever.bootstrap.router.get_intraday_stock import IntradayStockRouter


class Container:
    def __init__(self):
        self._application_configuration: AppConfiguration = load_application_configuration()
        self._create_http_client()

    @property
    def application_configuration(self) -> AppConfiguration:
        return self._application_configuration

    def _create_http_client(self) -> None:
        self._alpha_vantage_telemetry = OpenTelemetryManager(service_name="alpha-vantage")
        self._alpha_vantage_client = AlphaVantageClientFactory(
            self._application_configuration, self._alpha_vantage_telemetry
        ).create()

    async def start(self) -> None:
        await self._alpha_vantage_client.start()

    async def stop(self) -> None:
        await self._alpha_vantage_client.close()
        self._alpha_vantage_telemetry.shutdown()

    def build_intraday_stock_router(self) -> APIRouter:
        adapter: MarketDataFetcher = AlphaVantageMarketDataFetcher(client=self._alpha_vantage_client, mapper=Mapper)
        use_case: GetIntradayStock = GetIntradayStockUseCase(adapter)
        controller = IntradayStockController(use_case)
        router = IntradayStockRouter(controller).router

        return router
