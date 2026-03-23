from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class MetricDefinitionResponseEntry:
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


@dataclass(frozen=True)
class CreateMetricDefinitionResponse:
    metric_definition: MetricDefinitionResponseEntry


@dataclass(frozen=True)
class UpdateMetricDefinitionResponse:
    metric_definition: MetricDefinitionResponseEntry


@dataclass(frozen=True)
class ListMetricDefinitionsResponse:
    metric_definitions: list[MetricDefinitionResponseEntry]


@dataclass(frozen=True)
class ConversionDefinitionResponseEntry:
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


@dataclass(frozen=True)
class CreateConversionDefinitionResponse:
    conversion_definition: ConversionDefinitionResponseEntry


@dataclass(frozen=True)
class UpdateConversionDefinitionResponse:
    conversion_definition: ConversionDefinitionResponseEntry


@dataclass(frozen=True)
class ListConversionDefinitionsResponse:
    conversion_definitions: list[ConversionDefinitionResponseEntry]


@dataclass(frozen=True)
class ParamDefinitionResponseEntry:
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


@dataclass(frozen=True)
class CreateParamDefinitionResponse:
    param_definition: ParamDefinitionResponseEntry


@dataclass(frozen=True)
class UpdateParamDefinitionResponse:
    param_definition: ParamDefinitionResponseEntry


@dataclass(frozen=True)
class ListParamDefinitionsResponse:
    param_definitions: list[ParamDefinitionResponseEntry]


@dataclass(frozen=True)
class SecretTemplateResponseEntry:
    code: str
    display_name: str
    scope: str
    value_type: str
    is_masked: bool = True
    is_required: bool = False
    template_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass(frozen=True)
class CreateSecretTemplateResponse:
    secret_template: SecretTemplateResponseEntry


@dataclass(frozen=True)
class ListSecretTemplatesResponse:
    secret_templates: list[SecretTemplateResponseEntry]


@dataclass(frozen=True)
class GetSecretTemplatesResponse:
    secret_templates: SecretTemplateResponseEntry


@dataclass(frozen=True)
class AppSecretResponseEntry:
    template_id: int
    display_name: str
    value: str
    platform_id: int | None = None
    active_flag: bool = True
    version: float = 1
    secret_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass(frozen=True)
class CreateAppSecretResponse:
    app_secret: AppSecretResponseEntry


@dataclass(frozen=True)
class UpdateAppSecretResponse:
    app_secret: AppSecretResponseEntry


@dataclass(frozen=True)
class ListAppSecretsResponse:
    app_secrets: list[AppSecretResponseEntry]

@dataclass(frozen=True)
class GetAppSecretResponse:
    app_secret: AppSecretResponseEntry
    


@dataclass(frozen=True)
class ClickLogResponseEntry:
    click_id: str
    app_platform_id: int
    status: str = "accepted"
    raw_query: dict[str, Any] | None = None
    ip_address: str | None = None
    user_agent: str | None = None
    geo: dict[str, Any] | None = None
    referrer: str | None = None
    source: str | None = None
    redirect_target: str | None = None
    normalized_params: dict[str, Any] | None = None
    created_at: datetime | None = None


@dataclass(frozen=True)
class ListClickLogsResponse:
    clicks: list[ClickLogResponseEntry]


@dataclass(frozen=True)
class RawEventLogResponseEntry:
    event_id: str
    click_id: str
    event_type: str
    event_key: str
    event_time_utc: datetime
    app_user_id: int | None = None
    amount: float | None = None
    currency: str | None = None
    amount_usd: float | None = None
    payload: dict[str, Any] | None = None
    created_at: datetime | None = None


@dataclass(frozen=True)
class ListRawEventsResponse:
    events: list[RawEventLogResponseEntry]


@dataclass(frozen=True)
class AuditLogResponseEntry:
    entity_changed: str
    user_id: int | None = None
    app_id: int | None = None
    entity_id: str | None = None
    old_value: dict[str, Any] | list[Any] | None = None
    new_value: dict[str, Any] | list[Any] | None = None
    changed_at: datetime | None = None
    audit_log_id: int | None = None


@dataclass(frozen=True)
class ListAuditLogsResponse:
    audit_logs: list[AuditLogResponseEntry]
