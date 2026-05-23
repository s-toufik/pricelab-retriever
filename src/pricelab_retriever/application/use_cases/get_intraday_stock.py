from typing import Sequence, Optional
from pricelab_core.domain.model.candles.candle import Candle

from pricelab_retriever.application.port.outbound.market_data_fetcher import MarketDataFetcher


class GetIntradayStockUseCase:
    def __init__(self, market_data_fetcher: MarketDataFetcher) -> None:
        self._fetcher = market_data_fetcher

    async def __call__(self, symbol: str, interval: Optional[str]) -> Sequence[Candle]:
        return await self._fetcher.fetch_intraday(symbol=symbol, interval=interval)
