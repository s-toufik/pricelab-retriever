from pricelab_core.domain.model.candles.candle_series import CandleSeries

from pricelab_retriever.application.port.outbound.market_data_fetcher import MarketDataFetcher


class GetIntradayStockUseCase:
    def __init__(self, market_data_fetcher: MarketDataFetcher) -> None:
        self._fetcher = market_data_fetcher

    async def __call__(self, symbol: str, interval: str) -> CandleSeries:

        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": symbol,
            "interval": interval,
            "apikey": "demo",
        }
        return await self._fetcher.fetch_intraday(symbol=symbol, params=params)
