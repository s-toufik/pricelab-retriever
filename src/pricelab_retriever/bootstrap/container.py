from pricelab_core.infrastructure.app_configuration.model.configuration import AppConfiguration
from pricelab_core.infrastructure.telemetry.adapter.open_telemetry import OpenTelemetryManager

from pricelab_retriever.adapter.inbound.rest.router.intraday_stock_router import IntradayStock
from pricelab_retriever.adapter.outbound.alpha_vantage.adapter import AlphaVantageMarketDataFetcher
from pricelab_retriever.adapter.outbound.alpha_vantage.factory import AlphaVantageClientFactory
from pricelab_retriever.adapter.outbound.alpha_vantage.mapper import Mapper
from pricelab_retriever.application.port.inbound.get_intraday_stock import GetIntradayStock
from pricelab_retriever.application.port.outbound.market_data_fetcher import MarketDataFetcher
from pricelab_retriever.application.use_cases.get_intraday_stock import GetIntradayStockUseCase
from pricelab_retriever.bootstrap.application_configuration.load_application_configuration import (
    load_application_configuration,
)


class Container:
    def __init__(self):
        self._application_configuration: AppConfiguration = load_application_configuration()
        self._create_http_client()

    @property
    def application_configuration(self):
        return self._application_configuration

    def _create_http_client(self) -> None:
        self.alpha_vantage_client = AlphaVantageClientFactory(
            self._application_configuration, OpenTelemetryManager(service_name="alpha-vantage")
        ).create()

    def build_intraday_stock_controller(self):

        adapter: MarketDataFetcher = AlphaVantageMarketDataFetcher(client=self.alpha_vantage_client, mapper=Mapper)
        use_case: GetIntradayStock = GetIntradayStockUseCase(adapter)
        return IntradayStock(use_case)

    async def start(self):
        await self.alpha_vantage_client.start()

    async def stop(self):
        await self.alpha_vantage_client.close()
