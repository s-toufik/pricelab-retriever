from dataclasses import dataclass
from typing import Protocol, Optional, Iterator

from pricelab_core.domain.model.candles.candle import Candle


@dataclass(frozen=True, slots=True)
class MarketCandleQuery:
    symbol: str
    interval: Optional[str]


class MarketCandle(Protocol):
    async def fetch(self, query: MarketCandleQuery) -> Iterator[Candle]: ...
