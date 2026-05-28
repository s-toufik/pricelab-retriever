from enum import Enum
from typing import TypeVar, Iterator, overload, Literal

from pricelab_core.domain.model.candles.candle import Candle
from pricelab_core.domain.model.quotes.quote import Quote

from pricelab_retriever.application.port.outbound.market_data_mapper import MarketDataMapper

T = TypeVar('T')

class MapperStrategy(Enum):
    Candle = "candle"
    Quote = "quote"

class AlphaVantageMapper:
    @overload
    @staticmethod
    def create(strategy: Literal[MapperStrategy.Candle]) -> MarketDataMapper[dict, Candle]: ...
    @overload
    @staticmethod
    def create(strategy: Literal[MapperStrategy.Quote]) -> MarketDataMapper[dict, Quote]: ...

    @staticmethod
    def create(strategy: MapperStrategy) -> MarketDataMapper:
        match strategy:
            case MapperStrategy.Candle:
                return CandleMapper()
            case MapperStrategy.Quote:
                raise NotImplemented
            case _:
                raise ValueError(f"Unsupported strategy: {strategy}")


class CandleMapper:
    @staticmethod
    def map(source: dict) -> Iterator[Candle]:
        time_series_key = next(
            (key for key in source.keys() if "time series" in key.lower()),
            None,
        )

        if time_series_key is None:
            return

        symbol = source["Meta Data"]["2. Symbol"]
        time_series = source[time_series_key]

        for timestamp, values in time_series.items():
            yield Candle(
                symbol=symbol,
                timestamp=timestamp,
                source="alpha_vantage",
                open=float(values["1. open"]),
                high=float(values["2. high"]),
                low=float(values["3. low"]),
                close=float(values["4. close"]),
                volume=float(values["5. volume"]),
            )