from typing import Sequence, Iterator
from pricelab_core.domain.model.candles.candle import Candle

from pricelab_retriever.adapter.inbound.rest.schema.candle_schema import CandleSchema


class CandleSchemaMapper:
    @staticmethod
    def map(source: Sequence[Candle]) -> Iterator[CandleSchema]:
        for item in source:
            yield CandleSchema(
                source=item.source,
                symbol=item.symbol,
                timestamp=item.timestamp,
                open=item.open,
                high=item.high,
                low=item.low,
                close=item.close,
                volume=item.volume,
            )
