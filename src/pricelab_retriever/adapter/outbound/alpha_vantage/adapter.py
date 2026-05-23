from typing import Dict, Type, Sequence, Optional

from pricelab_core.domain.model.candles.candle import Candle
from pricelab_core.infrastructure.http.port.resilient_http_client import ResilientHttpClient

from pricelab_retriever.adapter.outbound.alpha_vantage.mapper import AlphaVantageMapper
from pricelab_retriever.adapter.outbound.alpha_vantage.settings import AlphaVantageSettings


class AlphaVantageMarketDataFetcher:
    def __init__(self, client: ResilientHttpClient, settings: AlphaVantageSettings, mapper: Type[AlphaVantageMapper]):
        self._client = client
        self._settings = settings
        self._mapper = mapper

    async def fetch_intraday(self, symbol: str, interval: Optional[str]) -> Sequence[Candle]:
        raw: dict = await self._client.get(self._get_path(), params=self._get_client_params(symbol, interval))
        return self._mapper.to_candles(raw)

    def _get_path(self) -> str:
        return self._settings.connector.base_url + self._settings.operation.endpoint

    def _get_client_params(self, symbol: str, interval: Optional[str]) -> Dict[str, str]:
        params = {
            **self._settings.operation.parameters,
            self._settings.auth.key_name: self._settings.auth.key_value,
            "symbol": symbol,
        }

        if interval is not None:
            params["interval"] = interval
        return params
