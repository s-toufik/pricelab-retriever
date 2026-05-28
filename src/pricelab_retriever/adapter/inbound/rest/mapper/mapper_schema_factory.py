from typing import overload, Literal

from pricelab_core.domain.model.candles.candle import Candle
from pricelab_core.domain.model.quotes.quote import Quote

from pricelab_retriever.adapter.inbound.rest.mapper.candle_schema_mapper import CandleSchemaMapper
from pricelab_retriever.adapter.inbound.rest.mapper.mapper_schema_strategy import MapperSchemaStrategy
from pricelab_retriever.adapter.inbound.rest.mapper.quote_schema_mapper import QuoteSchemaMapper
from pricelab_retriever.adapter.inbound.rest.mapper.schema_mapper import SchemaMapper
from pricelab_retriever.adapter.inbound.rest.schema.candle_schema import CandleSchema
from pricelab_retriever.adapter.inbound.rest.schema.quote_schema import QuoteSchema


class MapperSchemaFactory:

    @overload
    @staticmethod
    def create(strategy: Literal[MapperSchemaStrategy.Candle]) -> SchemaMapper[Candle, CandleSchema]: ...
    @overload
    @staticmethod
    def create(strategy: Literal[MapperSchemaStrategy.Quote]) -> SchemaMapper[Quote, QuoteSchema]: ...

    @staticmethod
    def create(strategy: MapperSchemaStrategy) -> SchemaMapper:
        match strategy:
            case MapperSchemaStrategy.Candle:
                return CandleSchemaMapper()
            case MapperSchemaStrategy.Quote:
                return QuoteSchemaMapper()
            case _:
                raise ValueError(f"Unsupported strategy: {strategy}")