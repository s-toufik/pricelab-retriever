from pricelab_core.domain.model.candles.candle_series import CandleSeries


class Mapper:
    @staticmethod
    def to_candle_series(raw: dict, symbol: str) -> CandleSeries:
        time_series_key = next(
            (k for k in raw if k.startswith("Time Series")),
            None,
        )

        if time_series_key is None:
            return CandleSeries(symbol=symbol, source="alpha_vantage")

        time_series = raw[time_series_key]

        times: list[str] = []
        opens: list[float] = []
        highs: list[float] = []
        lows: list[float] = []
        closes: list[float] = []
        volumes: list[float] = []

        for timestamp, values in time_series.items():
            times.append(timestamp)
            opens.append(float(values["1. open"]))
            highs.append(float(values["2. high"]))
            lows.append(float(values["3. low"]))
            closes.append(float(values["4. close"]))
            volumes.append(float(values["5. volume"]))

        typical_price = [
            (_open + _high + _low + _close) / 4 for _open, _high, _low, _close in zip(opens, highs, lows, closes)
        ]
        spread = [_high - _low for _high, _low in zip(highs, lows)]

        return CandleSeries(
            symbol=symbol,
            source="alpha_vantage",
            time=times,
            open=opens,
            high=highs,
            low=lows,
            close=closes,
            volumes=volumes,
            typical_price=typical_price,
            spread=spread,
        )
