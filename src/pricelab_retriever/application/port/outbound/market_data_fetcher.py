from typing import Protocol, Dict

from pricelab_core.domain.model.candles.candle_series import CandleSeries


class MarketDataFetcher(Protocol):
    async def fetch_intraday(self, symbol: str, params: Dict[str, str]) -> CandleSeries: ...
