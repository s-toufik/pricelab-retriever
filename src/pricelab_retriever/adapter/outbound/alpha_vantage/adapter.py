from typing import Dict, Sequence

from pricelab_core.domain.model.candles.candle import Candle
from pricelab_core.infrastructure.http.port.resilient_http_client import ResilientHttpClient

from pricelab_retriever.adapter.outbound.alpha_vantage.settings import AlphaVantageSettings
from pricelab_retriever.application.port.outbound.market_candle import MarketCandleQuery
from pricelab_retriever.application.port.outbound.market_mapper import MarketMapper


class AlphaVantageMarketCandle:
    def __init__(self, client: ResilientHttpClient, settings: AlphaVantageSettings, mapper: MarketMapper):
        self._client = client
        self._settings = settings
        self._mapper = mapper

    async def fetch(self, query: MarketCandleQuery) -> Sequence[Candle]:
        raw: dict = await self._client.get(self._get_path(), params=self._get_client_params(query))
        candles: Sequence[Candle] = tuple(self._mapper.map(raw))
        return candles

    def _get_path(self) -> str:
        return self._settings.connector.base_url + self._settings.operation.endpoint

    def _get_client_params(self, query: MarketCandleQuery) -> Dict[str, str]:
        params = {
            **self._settings.operation.parameters,
            self._settings.auth.key_name: self._settings.auth.key_value,
            "symbol": query.symbol,
        }

        if (interval := query.interval) is not None:
            params["interval"] = interval
        return params
