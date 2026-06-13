from dataclasses import dataclass
from datetime import datetime

from app.modules.crm.application.base import BaseResponse


class MetricDefinitionResponseEntry(BaseResponse):
    machine_key: str
    display_name: str
    app_id: int | None = None
    description: str | None = None
    enabled: bool = True
    visible_in_stats: bool = True
    visible_in_logs: bool = True
    metric_definition_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class CreateMetricDefinitionResponse(BaseResponse):
    metric_definition: MetricDefinitionResponseEntry


class UpdateMetricDefinitionResponse(BaseResponse):
    metric_definition: MetricDefinitionResponseEntry


class DeleteMetricDefinitionResponse(BaseResponse):
    metric_definition: MetricDefinitionResponseEntry


class GetMetricDefinitionResponse(BaseResponse):
    metric_definition: MetricDefinitionResponseEntry


class ListMetricDefinitionsResponse(BaseResponse):
    metric_definitions: list[MetricDefinitionResponseEntry]


class ConversionDefinitionResponseEntry(BaseResponse):
    machine_key: str
    display_name: str
    app_id: int | None = None
    description: str | None = None
    revenue_enabled: bool = False
    expects_amount: bool = False
    expects_currency: bool = False
    dedup_mode: str = "none"
    conversion_definition_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class CreateConversionDefinitionResponse(BaseResponse):
    conversion_definition: ConversionDefinitionResponseEntry


class UpdateConversionDefinitionResponse(BaseResponse):
    conversion_definition: ConversionDefinitionResponseEntry


class GetConversionDefinitionResponse(BaseResponse):
    conversion_definition: ConversionDefinitionResponseEntry


class DeleteConversionDefinitionResponse(BaseResponse):
    conversion_definition: ConversionDefinitionResponseEntry


class ListConversionDefinitionsResponse(BaseResponse):
    conversion_definitions: list[ConversionDefinitionResponseEntry]


class ParamDefinitionResponseEntry(BaseResponse):
    display_name: str
    machine_key: str
    data_type: str
    app_id: int | None = None
    description: str | None = None
    overwrite_policy: str = "replace"
    is_active: bool = True
    visible_in_logs: bool = True
    visible_in_stats: bool = False
    filterable: bool = False
    groupable: bool = False
    param_definition_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class CreateParamDefinitionResponse(BaseResponse):
    param_definition: ParamDefinitionResponseEntry


class DeleteParamDefinitionResponse(BaseResponse):
    param_definition: ParamDefinitionResponseEntry


class GetParamDefinitionResponse(BaseResponse):
    param_definition: ParamDefinitionResponseEntry


class UpdateParamDefinitionResponse(BaseResponse):
    param_definition: ParamDefinitionResponseEntry


class ListParamDefinitionsResponse(BaseResponse):
    param_definitions: list[ParamDefinitionResponseEntry]
