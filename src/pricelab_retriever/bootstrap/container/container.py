from functools import cached_property

from fastapi import APIRouter
from pricelab_core.domain.model.candles.candle import Candle
from pricelab_core.infrastructure.app_configuration.model.configuration import AppConfiguration
from pricelab_core.infrastructure.http.port.resilient_http_client import ResilientHttpClient
from pricelab_core.infrastructure.telemetry.port.telemetry import Telemetry

from pricelab_retriever.adapter.inbound.rest.controller.stock_candle_controller import StockCandleController
from pricelab_retriever.adapter.inbound.rest.mapper.mapper_schema_factory import MapperSchemaFactory
from pricelab_retriever.adapter.inbound.rest.mapper.mapper_schema_strategy import MapperSchemaStrategy
from pricelab_retriever.adapter.inbound.rest.mapper.schema_mapper import SchemaMapper
from pricelab_retriever.adapter.inbound.rest.schema.candle_schema import CandleSchema
from pricelab_retriever.adapter.outbound.alpha_vantage.adapter import AlphaVantageMarketCandle
from pricelab_retriever.adapter.outbound.alpha_vantage.factory import AlphaVantageFactory
from pricelab_retriever.adapter.outbound.alpha_vantage.mapper import AlphaVantageMapper, MapperStrategy
from pricelab_retriever.adapter.outbound.alpha_vantage.settings import AlphaVantageSettings
from pricelab_retriever.application.port.outbound.market_mapper import MarketMapper
from pricelab_retriever.application.port.inbound.stock_candle import StockCandle
from pricelab_retriever.application.port.outbound.market_candle import MarketCandle
from pricelab_retriever.application.use_case.stock_candle_use_case import StockCandleUseCase
from pricelab_retriever.bootstrap.application_configuration.load_application_configuration import (
    LoadApplicationConfiguration,
)
from pricelab_retriever.bootstrap.router.stock_candle_router import StockCandleRouter


class Container:
    # -------------------------------------------------------------------------
    # Core
    # -------------------------------------------------------------------------

    @cached_property
    def _configuration(self) -> AppConfiguration:
        return LoadApplicationConfiguration()()

    # -------------------------------------------------------------------------
    # Infrastructure — Alpha Vantage
    # -------------------------------------------------------------------------

    @cached_property
    def _alpha_vantage_settings(self) -> AlphaVantageSettings:
        return AlphaVantageSettings(self._configuration)

    @cached_property
    def _alpha_vantage_factory(self) -> AlphaVantageFactory:
        return AlphaVantageFactory(self._alpha_vantage_settings)

    @cached_property
    def _alpha_vantage_telemetry(self) -> Telemetry:
        return self._alpha_vantage_factory.telemetry

    @cached_property
    def _alpha_vantage_client(self) -> ResilientHttpClient:
        return self._register(self._alpha_vantage_factory.resilient_client)

    @cached_property
    def _alpha_vantage_mapper(self) -> MarketMapper[dict, Candle]:
        return AlphaVantageMapper().create(MapperStrategy.Candle)

    @cached_property
    def _alpha_vantage_adapter(self) -> MarketCandle:
        return AlphaVantageMarketCandle(
            client=self._alpha_vantage_client,
            settings=self._alpha_vantage_settings,
            mapper=self._alpha_vantage_mapper,
        )

    # -------------------------------------------------------------------------
    # Use cases
    # -------------------------------------------------------------------------

    @cached_property
    def _stock_candle_use_case(self) -> StockCandle:
        return StockCandleUseCase(self._alpha_vantage_adapter)

    # -------------------------------------------------------------------------
    # Routers
    # -------------------------------------------------------------------------

    @cached_property
    def stock_candle_router(self) -> APIRouter:
        mapper: SchemaMapper[Candle, CandleSchema] = MapperSchemaFactory().create(MapperSchemaStrategy.Candle)
        controller = StockCandleController(self._stock_candle_use_case, mapper)
        return StockCandleRouter(controller).router

    # -------------------------------------------------------------------------
    # Lifecycle
    # -------------------------------------------------------------------------

    def __init__(self) -> None:
        self._clients: list[ResilientHttpClient] = []
        self._telemetries: list[Telemetry] = []

    def _register(self, client: ResilientHttpClient) -> ResilientHttpClient:
        self._clients.append(client)
        return client

    def _register_telemetry(self, telemetry: Telemetry) -> Telemetry:
        self._telemetries.append(telemetry)
        return telemetry

    async def start(self) -> None:
        for client in self._clients:
            await client.start()

    async def stop(self) -> None:
        for client in self._clients:
            await client.close()
        for telemetry in self._telemetries:
            telemetry.shutdown()
