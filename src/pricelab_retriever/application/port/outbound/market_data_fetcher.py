from typing import Protocol, Dict, Sequence

from pricelab_core.domain.model.candles.candle import Candle

class MarketDataFetcher(Protocol):
    async def fetch_intraday(self, symbol: str, params: Dict[str, str]) ->  Sequence[Candle]: ...
