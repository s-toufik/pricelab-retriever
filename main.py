from pprint import pprint
import asyncio

from pricelab_core.infrastructure.http.adapter.aiohttp_client import AioHttpClient
from pricelab_core.infrastructure.http.adapter.circuit_breaker_policy import CircuitBreakerPolicy
from pricelab_core.infrastructure.http.adapter.resilient_client import ResilientClient
from pricelab_core.infrastructure.http.adapter.retry_policy import RetryPolicy
from pricelab_core.infrastructure.http.port.resilient_http_client import ResilientHttpClient
from pricelab_core.infrastructure.http.port.retry import Retry
from pricelab_core.infrastructure.http.port.http_client import HttpClient
from pricelab_core.infrastructure.telemetry.adapter.open_telemetry import OpenTelemetryManager
from pricelab_core.infrastructure.telemetry.port.telemetry import Telemetry

from pricelab_retriever.bootstrap.application_configuration.load_application_configuration import (
    load_application_configuration,
)


async def main():

    app_configuration = load_application_configuration()
    pprint(app_configuration)

    telemetry: Telemetry = OpenTelemetryManager(service_name="alpha-vantage")

    base_client: HttpClient = AioHttpClient(
        base_url="https://www.alphavantage.co",
    )

    retry_policy: Retry = RetryPolicy()

    circuit_breaker: CircuitBreakerPolicy = CircuitBreakerPolicy()

    client: ResilientHttpClient = ResilientClient(
        base_client=base_client,
        circuit_breaker=circuit_breaker,
        retry_policy=retry_policy,
        trace_manager=telemetry,
    )

    try:
        await base_client.start()

        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": "IBM",
            "interval": "5min",
            "apikey": "demo",
        }

        response = await client.get(
            "/query",
            params=params,
        )

        print(response)
    finally:
        await base_client.close()

        telemetry.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
