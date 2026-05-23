from typing import Protocol, Sequence, Optional

from pricelab_core.domain.model.candles.candle import Candle


class MarketDataFetcher(Protocol):
    async def fetch_intraday(self, symbol: str, interval: Optional[str]) -> Sequence[Candle]: ...
