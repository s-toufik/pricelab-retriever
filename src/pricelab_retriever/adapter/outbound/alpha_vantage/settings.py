from typing import cast

from pricelab_core.infrastructure.app_configuration.enum.connector_type import ConnectorType
from pricelab_core.infrastructure.app_configuration.enum.run_type_environment import RunTypeEnvironment
from pricelab_core.infrastructure.app_configuration.model.configuration import AppConfiguration
from pricelab_core.infrastructure.app_configuration.model.connector import ApiConnector, TelemetryConnector
from pricelab_core.infrastructure.app_configuration.model.operation import ApiOperation
from pricelab_core.infrastructure.authentication import TokenAuth


class AlphaVantageSettings:
    def __init__(self, application_configuration: AppConfiguration) -> None:
        self._application_configuration = application_configuration

    @property
    def telemetry(self) -> TelemetryConnector:
        return self._get_telemetry()

    @property
    def run_type_environment(self) -> RunTypeEnvironment:
        return self._get_run_type_environment()

    @property
    def base_url(self) -> str:
        return self._get_connector().base_url

    @property
    def connector(self) -> ApiConnector:
        return self._get_connector()

    @property
    def operation(self) -> ApiOperation:
        return self._get_operation()

    @property
    def auth(self) -> TokenAuth:
        return self._get_auth()

    def _get_run_type_environment(self) -> RunTypeEnvironment:
        return self._application_configuration.env

    def _get_telemetry(self) -> TelemetryConnector:
        return cast(
            TelemetryConnector, self._application_configuration.connector[ConnectorType.telemetry]["open_telemetry"]
        )

    def _get_connector(self) -> ApiConnector:
        return cast(ApiConnector, self._application_configuration.connector[ConnectorType.api]["alpha_vantage"])

    def _get_operation(self) -> ApiOperation:
        return cast(ApiOperation, self._application_configuration.operation.get("alpha_vantage_intraday_stock"))

    def _get_auth(self) -> TokenAuth:
        return cast(TokenAuth, self._get_connector().auth)
