from typing import Protocol

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
    CreateConversionDefinitionResponse,
    CreateMetricDefinitionResponse,
    CreateParamDefinitionResponse,
    DeleteConversionDefinitionResponse,
    DeleteMetricDefinitionResponse,
    DeleteParamDefinitionResponse,
    GetConversionDefinitionResponse,
    GetMetricDefinitionResponse,
    GetParamDefinitionResponse,
    ListConversionDefinitionsResponse,
    ListMetricDefinitionsResponse,
    ListParamDefinitionsResponse,
    UpdateConversionDefinitionResponse,
    UpdateMetricDefinitionResponse,
    UpdateParamDefinitionResponse,
)


class DefinitionsServiceProtocol(Protocol):
    def list_metrics(
        self,
        command: ListMetricDefinitionsCommand,
    ) -> ListMetricDefinitionsResponse: ...

    def get_metric_definition(
        self,
        command: GetMetricDefinitionCommand,
    ) -> GetMetricDefinitionResponse: ...

    def update_metric_definition(
        self,
        command: UpdateMetricDefinitionCommand,
    ) -> UpdateMetricDefinitionResponse: ...

    def delete_metric_definition(
        self,
        command: DeleteMetricDefinitionCommand,
    ) -> DeleteMetricDefinitionResponse: ...

    def create_metric_definition(
        self,
        command: CreateMetricDefinitionCommand,
    ) -> CreateMetricDefinitionResponse: ...

    def list_conversions(
        self,
        command: ListConversionDefinitionsCommand,
    ) -> ListConversionDefinitionsResponse: ...

    def get_conversion_definition(
        self,
        command: GetConversionDefinitionCommand,
    ) -> GetConversionDefinitionResponse: ...

    def update_conversion_definition(
        self,
        command: UpdateConversionDefinitionCommand,
    ) -> UpdateConversionDefinitionResponse: ...

    def create_conversion_definition(
        self,
        command: CreateConversionDefinitionCommand,
    ) -> CreateConversionDefinitionResponse: ...

    def delete_conversion_definition(
        self,
        command: DeleteConversionDefinitionCommand,
    ) -> DeleteConversionDefinitionResponse: ...

    def list_params(
        self,
        command: ListParamDefinitionsCommand,
    ) -> ListParamDefinitionsResponse: ...

    def get_param_definition(
        self,
        command: GetParamDefinitionCommand,
    ) -> GetParamDefinitionResponse: ...

    def update_param_definition(
        self,
        command: UpdateParamDefinitionCommand,
    ) -> UpdateParamDefinitionResponse: ...

    def create_param_definition(
        self,
        command: CreateParamDefinitionCommand,
    ) -> CreateParamDefinitionResponse: ...

    def delete_param_definition(
        self,
        command: DeleteParamDefinitionCommand,
    ) -> DeleteParamDefinitionResponse: ...
