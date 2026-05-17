from typing import Protocol, Sequence

from pricelab_core.domain.model.candles.candle import Candle


class GetIntradayStock(Protocol):
    async def __call__(self, symbol: str, interval: str) -> Sequence[Candle]: ...
