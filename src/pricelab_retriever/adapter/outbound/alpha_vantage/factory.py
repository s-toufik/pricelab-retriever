from typing import cast

from pricelab_core.infrastructure.app_configuration.enum.connector_type import ConnectorType
from pricelab_core.infrastructure.app_configuration.model.configuration import AppConfiguration
from pricelab_core.infrastructure.app_configuration.model.connector import ApiConnector

from pricelab_core.infrastructure.http.configuration.circuite_breaker_configuration import CircuitBreakerSettings
from pricelab_core.infrastructure.http.configuration.retry_configuration import RetrySettings

from pricelab_core.infrastructure.http.adapter.aiohttp_client import AioHttpClient
from pricelab_core.infrastructure.http.adapter.circuit_breaker_policy import CircuitBreakerPolicy
from pricelab_core.infrastructure.http.adapter.resilient_client import ResilientClient
from pricelab_core.infrastructure.http.adapter.retry_policy import RetryPolicy

from pricelab_core.infrastructure.http.port.resilient_http_client import ResilientHttpClient
from pricelab_core.infrastructure.http.port.retry import Retry
from pricelab_core.infrastructure.http.port.http_client import HttpClient

from pricelab_core.infrastructure.telemetry.port.telemetry import Telemetry


class AlphaVantageClientFactory:
    def __init__(self, configuration: AppConfiguration, telemetry: Telemetry) -> None:

        self._configuration = configuration
        self._telemetry = telemetry

    def create(self) -> ResilientHttpClient:
        api_configuration = self._load_configuration()
        base_client = self._create_base_client(api_configuration)
        retry_policy = self._create_retry_policy(api_configuration)
        circuit_breaker = self._create_circuit_breaker(api_configuration)

        return ResilientClient(
            base_client=base_client,
            retry_policy=retry_policy,
            circuit_breaker=circuit_breaker,
            trace_manager=self._telemetry,
        )

    def _load_configuration(self) -> ApiConnector:
        connector = self._configuration.connector
        api_configuration = cast(ApiConnector, connector[ConnectorType.api]["alpha_vantage"])
        if api_configuration is None:
            raise ValueError("Alpha Vantage configuration is missing")
        return api_configuration

    @staticmethod
    def _create_base_client(api_configuration: ApiConnector) -> HttpClient:
        return AioHttpClient(base_url=api_configuration.base_url, timeout=api_configuration.timeout)

    @staticmethod
    def _create_retry_policy(api_configuration: ApiConnector) -> Retry:
        settings = RetrySettings()
        settings.retries = api_configuration.retry

        return RetryPolicy(settings)

    @staticmethod
    def _create_circuit_breaker(api_configuration: ApiConnector) -> CircuitBreakerPolicy:
        settings = CircuitBreakerSettings()
        settings.failure_threshold = max(1, api_configuration.retry - 1)
        return CircuitBreakerPolicy(settings)
