from typing import Mapping

from app.core.utils.general_mapper import GeneralMapper
from app.modules.crm.application.admin.definitions.commands import (
    CreateConversionDefinitionCommand,
    CreateMetricDefinitionCommand,
    CreateParamDefinitionCommand,
    DeleteConversionDefinitionCommand,
    DeleteMetricDefinitionCommand,
    DeleteParamDefinitionCommand,
    GetConversionDefinitionCommand,
    GetMetricDefinitionCommand,
    GetParamDefinitionCommand,
    ListConversionDefinitionsCommand,
    ListMetricDefinitionsCommand,
    ListParamDefinitionsCommand,
    UpdateConversionDefinitionCommand,
    UpdateMetricDefinitionCommand,
    UpdateParamDefinitionCommand,
)
from app.modules.crm.application.admin.definitions.responses import (
    ConversionDefinitionResponseEntry,
    MetricDefinitionResponseEntry,
    ParamDefinitionResponseEntry,
)
from app.modules.crm.domain.conversion_definition.CrmConversionDefinitionEntity import CrmConversionDefinitionEntity
from app.modules.crm.domain.metric_definition.CrmMetricDefinitionEntity import CrmMetricDefinitionEntity
from app.modules.crm.domain.param_definition.CrmParamDefinitionEntity import CrmParamDefinitionEntity


class DefinitionsCommandsMapper:
    @classmethod
    def list_metrics_from_transport(cls, payload: Mapping[str, object]) -> ListMetricDefinitionsCommand:
        return GeneralMapper.command_payload_to_command(ListMetricDefinitionsCommand, payload)

    @classmethod
    def get_metric_from_transport(cls, payload: Mapping[str, object]) -> GetMetricDefinitionCommand:
        return GeneralMapper.command_payload_to_command(GetMetricDefinitionCommand, payload)

    @classmethod
    def create_metric_from_transport(cls, payload: Mapping[str, object]) -> CreateMetricDefinitionCommand:
        return GeneralMapper.command_payload_to_command(CreateMetricDefinitionCommand, payload)

    @classmethod
    def update_metric_from_transport(cls, payload: Mapping[str, object]) -> UpdateMetricDefinitionCommand:
        return GeneralMapper.command_payload_to_command(UpdateMetricDefinitionCommand, payload)

    @classmethod
    def delete_metric_from_transport(cls, payload: Mapping[str, object]) -> DeleteMetricDefinitionCommand:
        return GeneralMapper.command_payload_to_command(DeleteMetricDefinitionCommand, payload)

    @classmethod
    def list_conversions_from_transport(cls, payload: Mapping[str, object]) -> ListConversionDefinitionsCommand:
        return GeneralMapper.command_payload_to_command(ListConversionDefinitionsCommand, payload)

    @classmethod
    def get_conversion_from_transport(cls, payload: Mapping[str, object]) -> GetConversionDefinitionCommand:
        return GeneralMapper.command_payload_to_command(GetConversionDefinitionCommand, payload)

    @classmethod
    def create_conversion_from_transport(cls, payload: Mapping[str, object]) -> CreateConversionDefinitionCommand:
        return GeneralMapper.command_payload_to_command(CreateConversionDefinitionCommand, payload)

    @classmethod
    def update_conversion_from_transport(cls, payload: Mapping[str, object]) -> UpdateConversionDefinitionCommand:
        return GeneralMapper.command_payload_to_command(UpdateConversionDefinitionCommand, payload)

    @classmethod
    def delete_conversion_from_transport(cls, payload: Mapping[str, object]) -> DeleteConversionDefinitionCommand:
        return GeneralMapper.command_payload_to_command(DeleteConversionDefinitionCommand, payload)

    @classmethod
    def list_params_from_transport(cls, payload: Mapping[str, object]) -> ListParamDefinitionsCommand:
        return GeneralMapper.command_payload_to_command(ListParamDefinitionsCommand, payload)

    @classmethod
    def get_param_from_transport(cls, payload: Mapping[str, object]) -> GetParamDefinitionCommand:
        return GeneralMapper.command_payload_to_command(GetParamDefinitionCommand, payload)

    @classmethod
    def create_param_from_transport(cls, payload: Mapping[str, object]) -> CreateParamDefinitionCommand:
        return GeneralMapper.command_payload_to_command(CreateParamDefinitionCommand, payload)

    @classmethod
    def update_param_from_transport(cls, payload: Mapping[str, object]) -> UpdateParamDefinitionCommand:
        return GeneralMapper.command_payload_to_command(UpdateParamDefinitionCommand, payload)

    @classmethod
    def delete_param_from_transport(cls, payload: Mapping[str, object]) -> DeleteParamDefinitionCommand:
        return GeneralMapper.command_payload_to_command(DeleteParamDefinitionCommand, payload)


class DefinitionsResponseMapper:
    @classmethod
    def conversion_domain_to_value(cls, domain: CrmConversionDefinitionEntity) -> ConversionDefinitionResponseEntry:
        return ConversionDefinitionResponseEntry.model_validate(domain)

    @classmethod
    def metric_domain_to_value(cls, domain: CrmMetricDefinitionEntity) -> MetricDefinitionResponseEntry:
        return MetricDefinitionResponseEntry.model_validate(domain)

    @classmethod
    def param_domain_to_value(cls, domain: CrmParamDefinitionEntity) -> ParamDefinitionResponseEntry:
        return ParamDefinitionResponseEntry.model_validate(domain)
