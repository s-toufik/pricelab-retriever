from typing import Dict, Type, Sequence

from pricelab_core.domain.model.candles.candle import Candle
from pricelab_core.infrastructure.http.port.resilient_http_client import ResilientHttpClient

from pricelab_retriever.adapter.outbound.alpha_vantage.mapper import Mapper


class AlphaVantageMarketDataFetcher:
    def __init__(self, client: ResilientHttpClient, mapper: Type[Mapper]):
        self._client = client
        self._mapper = mapper

    async def fetch_intraday(self, symbol: str, params: Dict[str, str]) ->  Sequence[Candle]:
        raw: dict = await self._client.get("/query", params=params)
        return self._mapper.to_candles(raw, symbol)
