from typing import Protocol, Sequence, Optional

from pricelab_core.domain.model.candles.candle import Candle


class GetIntradayStock(Protocol):
    async def __call__(self, symbol: str, interval: Optional[str]) -> Sequence[Candle]: ...
