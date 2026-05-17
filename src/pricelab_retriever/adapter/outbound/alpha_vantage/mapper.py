from typing import List

from pricelab_core.domain.model.candles.candle import Candle

class Mapper:

    @staticmethod
    def to_candles(raw: dict, symbol: str) -> List[Candle]:
        result: List[Candle] = []
        time_series_key = next(
            (k for k in raw if k.startswith("Time Series")),
            None,
        )

        if time_series_key is None:
            return result

        time_series = raw[time_series_key]

        for timestamp, values in time_series.items():
            result.append(
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
            )

        return result
