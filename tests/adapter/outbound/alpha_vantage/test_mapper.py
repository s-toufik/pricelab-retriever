import pytest
from typing import Iterator
from pricelab_core.domain.model.candles.candle import Candle
from pricelab_core.domain.model.quotes.quote import Quote
from pricelab_core.domain.service.candles.candle_validator import CandleValidator

from pricelab_retriever.adapter.outbound.alpha_vantage.mapper import AlphaVantageMapper, MapperStrategy
from pricelab_retriever.application.port.outbound.market_mapper import MarketMapper


class TestAlphaVantageMapper:
    @pytest.fixture
    def mapper(self) -> AlphaVantageMapper:
        return AlphaVantageMapper()

    @pytest.fixture
    def realistic_response(self) -> dict:
        return {
            "Meta Data": {
                "1. Information": "Weekly Prices (open, high, low, close) and Volumes",
                "2. Symbol": "IBM",
                "3. Last Refreshed": "2026-06-08",
                "4. Time Zone": "US/Eastern",
            },
            "Weekly Time Series": {
                "2026-06-08": {
                    "1. open": "286.4400",
                    "2. high": "290.5000",
                    "3. low": "279.4300",
                    "4. close": "280.8200",
                    "5. volume": "6790639",
                },
                "2026-06-05": {
                    "1. open": "322.5500",
                    "2. high": "332.4600",
                    "3. low": "281.0701",
                    "4. close": "284.8400",
                    "5. volume": "86135011",
                },
            },
        }

    @pytest.fixture
    def empty_response(self) -> dict:
        return {}

    def test_create_mapper(self, mapper) -> None:
        candle_mapper: MarketMapper[dict, Candle] = mapper.create(MapperStrategy.Candle)
        assert isinstance(candle_mapper, MarketMapper)
        quote_mapper: MarketMapper[dict, Quote] = mapper.create(MapperStrategy.Quote)
        assert isinstance(quote_mapper, MarketMapper)

    @pytest.fixture
    def create_candles(self, mapper, realistic_response) -> Iterator[Candle]:
        candle_mapper: MarketMapper[dict, Candle] = mapper.create(MapperStrategy.Candle)
        return candle_mapper.map(realistic_response)

    def test_map_to_candle(self, create_candles) -> None:
        assert isinstance(next(create_candles), Candle)

    def test_map_to_candle_valide(self, create_candles) -> None:
        assert CandleValidator().status(next(create_candles)).is_valid

    def test_map_to_candle_length(self, create_candles) -> None:
        assert len(list(create_candles)) == 2

    def test_map_to_empty_candle(self, mapper, empty_response) -> None:
        candle_mapper: MarketMapper[dict, Candle] = mapper.create(MapperStrategy.Candle)
        result = candle_mapper.map(empty_response)
        with pytest.raises(StopIteration):
            result.__next__()
