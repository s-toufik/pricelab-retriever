from dataclasses import dataclass
from typing import Protocol, Sequence, Optional

from pricelab_core.domain.model.candles.candle import Candle


@dataclass(frozen=True, slots=True)
class MarketQuoteQuery:
    symbol: str
    interval: Optional[str]


class MarketQuote(Protocol):
    async def fetch(self, query: MarketQuoteQuery) -> Sequence[Candle]: ...
