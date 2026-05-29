from dataclasses import dataclass
from typing import Protocol, Sequence, Optional

from pricelab_core.domain.model.candles.candle import Candle


@dataclass(frozen=True, slots=True)
class StockCandleQuery:
    symbol: str
    interval: Optional[str]


class StockCandle(Protocol):
    async def __call__(self, query: StockCandleQuery) -> Sequence[Candle]: ...
