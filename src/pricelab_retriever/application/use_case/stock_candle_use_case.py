from typing import Sequence, Iterator
from pricelab_core.domain.model.candles.candle import Candle

from pricelab_retriever.application.port.inbound.stock_candle import StockCandleQuery
from pricelab_retriever.application.port.outbound.market_candle import MarketCandle, MarketCandleQuery


class StockCandleUseCase:
    def __init__(self, candle_adapter: MarketCandle) -> None:
        self._candle_adapter = candle_adapter

    async def __call__(self, query: StockCandleQuery) -> Sequence[Candle]:
        _query = MarketCandleQuery(symbol=query.symbol, interval=query.interval)
        candles: Iterator[Candle] = await self._candle_adapter.fetch(_query)
        return tuple(candles)
