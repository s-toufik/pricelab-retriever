from fastapi import APIRouter
from pricelab_core.domain.model.candles.candle import Candle
from pricelab_core.infrastructure.app_configuration.model.configuration import AppConfiguration
from pricelab_core.infrastructure.http.port.resilient_http_client import ResilientHttpClient
from pricelab_core.infrastructure.telemetry.port.telemetry import Telemetry

from pricelab_retriever.adapter.inbound.rest.controller.get_intraday_stock import IntradayStockController
from pricelab_retriever.adapter.inbound.rest.mapper.mapper_schema_factory import MapperSchemaFactory
from pricelab_retriever.adapter.inbound.rest.mapper.mapper_schema_strategy import MapperSchemaStrategy
from pricelab_retriever.adapter.inbound.rest.mapper.schema_mapper import SchemaMapper
from pricelab_retriever.adapter.inbound.rest.schema.candle_schema import CandleSchema
from pricelab_retriever.adapter.outbound.alpha_vantage.adapter import AlphaVantageMarketDataFetcher
from pricelab_retriever.adapter.outbound.alpha_vantage.factory import AlphaVantageFactory
from pricelab_retriever.adapter.outbound.alpha_vantage.mapper import AlphaVantageMapper, MapperStrategy
from pricelab_retriever.adapter.outbound.alpha_vantage.settings import AlphaVantageSettings
from pricelab_retriever.application.port.outbound.market_data_mapper import MarketDataMapper
from pricelab_retriever.application.port.inbound.get_intraday_stock import GetIntradayStock
from pricelab_retriever.application.port.outbound.market_data_fetcher import MarketDataFetcher
from pricelab_retriever.application.use_cases.get_intraday_stock import GetIntradayStockUseCase
from pricelab_retriever.bootstrap.application_configuration.load_application_configuration import (
    LoadApplicationConfiguration,
)
from pricelab_retriever.bootstrap.router.get_intraday_stock import IntradayStockRouter


class Container:
    def __init__(self):
        self._application_configuration: AppConfiguration = LoadApplicationConfiguration()()
        self._create_http_client()

    @property
    def application_configuration(self) -> AppConfiguration:
        return self._application_configuration

    def _create_http_client(self) -> None:
        self._init_alpha_vantage()

    async def start(self) -> None:
        await self._alpha_vantage_client.start()

    async def stop(self) -> None:
        await self._alpha_vantage_client.close()
        self._alpha_vantage_telemetry.shutdown()

    def build_intraday_stock_router(self) -> APIRouter:
        use_case: GetIntradayStock = GetIntradayStockUseCase(self._alpha_vantage_adapter)
        mapper: SchemaMapper[Candle, CandleSchema] = MapperSchemaFactory().create(MapperSchemaStrategy.Candle)
        controller = IntradayStockController(use_case, mapper)
        router = IntradayStockRouter(controller).router

        return router

    def _init_alpha_vantage(self):
        alpha_vantage_settings = AlphaVantageSettings(self._application_configuration)
        alpha_vantage_factor = AlphaVantageFactory(alpha_vantage_settings)
        alpha_vantage_mapper: MarketDataMapper[dict, Candle] = AlphaVantageMapper().create(MapperStrategy.Candle)
        self._alpha_vantage_telemetry: Telemetry = alpha_vantage_factor.telemetry
        self._alpha_vantage_client: ResilientHttpClient = alpha_vantage_factor.resilient_client
        self._alpha_vantage_adapter: MarketDataFetcher = AlphaVantageMarketDataFetcher(
            client=self._alpha_vantage_client, settings=alpha_vantage_settings, mapper=alpha_vantage_mapper
        )
