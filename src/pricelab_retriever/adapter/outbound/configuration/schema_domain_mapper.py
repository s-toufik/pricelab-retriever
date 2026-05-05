from pricelab_retriever.adapter.outbound.configuration.schema import AppConfigurationSchema
from pricelab_retriever.application.port.outbound.schema_domain_mapper import SchemaToDomainMapper
from pricelab_retriever.domain.model.app.app_configuration import AppConfiguration


class MapperDomainSchema(SchemaToDomainMapper):

    def map_to_app_configuration(self, app_configuration_schema: AppConfigurationSchema) -> AppConfiguration:
        return AppConfiguration(**vars(app_configuration_schema))