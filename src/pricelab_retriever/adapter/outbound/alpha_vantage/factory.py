from functools import cached_property

from pricelab_core.infrastructure.http.configuration.circuite_breaker_configuration import CircuitBreakerSettings
from pricelab_core.infrastructure.http.configuration.retry_configuration import RetrySettings
from pricelab_core.infrastructure.http.adapter.aiohttp_client import AioHttpClient
from pricelab_core.infrastructure.http.adapter.circuit_breaker_policy import CircuitBreakerPolicy
from pricelab_core.infrastructure.http.adapter.resilient_client import ResilientClient
from pricelab_core.infrastructure.http.adapter.retry_policy import RetryPolicy
from pricelab_core.infrastructure.http.port.resilient_http_client import ResilientHttpClient
from pricelab_core.infrastructure.http.port.retry import Retry
from pricelab_core.infrastructure.http.port.http_client import HttpClient
from pricelab_core.infrastructure.telemetry.adapter.open_telemetry import OpenTelemetryManager
from pricelab_core.infrastructure.telemetry.port.telemetry import Telemetry

from pricelab_retriever.adapter.outbound.alpha_vantage.settings import AlphaVantageSettings


class AlphaVantageFactory:
    def __init__(self, settings: AlphaVantageSettings) -> None:
        self._settings = settings

    @cached_property
    def resilient_client(self) -> ResilientHttpClient:
        base_client = self._create_base_client()
        retry_policy = self._create_retry_policy()
        circuit_breaker = self._create_circuit_breaker()
        telemetry = self.telemetry

        return ResilientClient(
            base_client=base_client,
            retry_policy=retry_policy,
            circuit_breaker=circuit_breaker,
            trace_manager=telemetry,
        )

    @cached_property
    def telemetry(self) -> Telemetry:
        return OpenTelemetryManager(
            service_name=self._settings.connector.name,
            environment=self._settings.run_type_environment,
            otlp_endpoint=f"{self._settings.telemetry.host}:{self._settings.telemetry.port}",
        )

    def _create_base_client(self) -> HttpClient:
        return AioHttpClient(base_url=self._settings.connector.base_url, timeout=self._settings.connector.timeout)

    def _create_retry_policy(self) -> Retry:
        retry_settings = RetrySettings(
            retries=self._settings.connector.retry,
        )
        return RetryPolicy(retry_settings)

    def _create_circuit_breaker(self) -> CircuitBreakerPolicy:
        settings = CircuitBreakerSettings(
            failure_threshold=max(1, self._settings.connector.retry - 1)
        )
        return CircuitBreakerPolicy(settings)
