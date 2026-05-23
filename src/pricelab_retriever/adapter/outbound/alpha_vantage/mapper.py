from typing import List

from pricelab_core.domain.model.candles.candle import Candle


class AlphaVantageMapper:
    @staticmethod
    def to_candles(raw: dict) -> List[Candle]:
        result: List[Candle] = []
        time_series_key = next(
            (key for key in raw.keys() if "time series" in key.lower()),
            None,
        )

        if time_series_key is None:
            return result

        symbol = raw["Meta Data"]["2. Symbol"]
        time_series = raw[time_series_key]

        return [
            Candle(
                symbol=symbol,
                timestamp=timestamp,
                source="alpha_vantage",
                open=float(values["1. open"]),
                high=float(values["2. high"]),
                low=float(values["3. low"]),
                close=float(values["4. close"]),
                volume=float(values["5. volume"]),
            )
            for timestamp, values in time_series.items()
        ]
