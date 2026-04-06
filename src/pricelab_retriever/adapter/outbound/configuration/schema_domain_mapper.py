from typing import Dict, Any, List

from pricelab_core.adapter.outbound.serializer.dictionary_serializer import DictionarySerializer

from pricelab_retriever.adapter.outbound.configuration.schema import AppConfigurationSchema
from pricelab_retriever.application.port.outbound.schema_domain_mapper import BaseMapperDomainSchema
from pricelab_retriever.domain.model.app.app_configuration import AppBaseConfiguration, AppConfiguration
from pricelab_retriever.domain.model.authentication.authentication import AuthType, TokenAuth, BasicAuth
from pricelab_retriever.domain.model.external_api.api_configuration import ApiConfiguration, Endpoint

class MapperDomainSchema(BaseMapperDomainSchema):

    def map_to_domain(self, raw_configuration: Dict[str, Any]) -> AppConfiguration:
        app_raw_configuration = raw_configuration["app"]
        AppConfigurationSchema(**app_raw_configuration)
        base = DictionarySerializer.deserialize(app_raw_configuration["base"], AppBaseConfiguration)

        external_api_registry: List[ApiConfiguration] = []
        for external_api in app_raw_configuration["external_api_registery"]:

            if (auth := external_api["auth"])["type"] == AuthType.token.value:
                authentication = DictionarySerializer.deserialize(auth, TokenAuth)
            elif (auth := external_api["auth"])["type"] == AuthType.basic.value:
                authentication = DictionarySerializer.deserialize(auth, BasicAuth)
            else:
                authentication = None

            api_endpoints: List[Endpoint] = []
            for endpoint in external_api["endpoints"]:
                api_endpoints.append(DictionarySerializer.deserialize(endpoint, Endpoint))

            api_configuration = DictionarySerializer.deserialize(external_api, ApiConfiguration)
            external_api_registry.append(api_configuration)
            api_configuration.auth = authentication
            api_configuration.endpoints = api_endpoints

        return AppConfiguration(
            base,
            external_api_registry
        )