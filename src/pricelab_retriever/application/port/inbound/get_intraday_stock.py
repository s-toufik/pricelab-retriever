from typing import Protocol

from pricelab_core.domain.model.candles.candle_series import CandleSeries


class GetIntradayStock(Protocol):
    async def __call__(self, symbol: str, interval: str) -> CandleSeries: ...
