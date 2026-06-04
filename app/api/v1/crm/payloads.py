from __future__ import annotations

from typing import Any

from pydantic import Field

from app.api.v1.transport import TransportPayload
from app.application.base import JsonDict


class AppScopeQueryPayload(TransportPayload):
    app_id: int


class AppFilterQueryPayload(TransportPayload):
    app_id: int | None = None


class CreateAppPayload(TransportPayload):
    code_slug: str
    name: str
    description: str | None = None
    is_active: bool = True


class UpdateAppPayload(TransportPayload):
    app_id: int
    code_slug: str | None = None
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


class DeleteAppPayload(TransportPayload):
    app_id: int


class CreateAppPlatformPayload(TransportPayload):
    app_id: int
    platform: str
    install_key: str 
    is_active: bool = True


class UpdateAppPlatformPayload(TransportPayload):
    platform: str | None = None
    install_key: str | None = None
    is_active: bool | None = None


class UpdateMetricDefinitionPayload(TransportPayload):
    key: str | None = None
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


class CreateMetricDefinitionPayload(TransportPayload):
    app_id: int
    key: str
    name: str
    description: str | None = None
    is_active: bool = True


class CreateConversionDefinitionPayload(TransportPayload):
    app_id: int
    key: str
    name: str
    description: str | None = None
    revenue_enabled: bool = True
    expects_amount: bool = True
    expects_currency: bool = True
    dedup_mode: str | None = None
    is_active: bool = True

class UpdateConversionDefinitionPayload(TransportPayload):
    key: str | None = None
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


class CreateParamDefinitionPayload(TransportPayload):
    app_id: int
    key: str
    label: str
    param_type: str
    description: str | None = None
    is_required: bool = False
    overwrite_policy: str | None = None
    is_active: bool | None = None
    visible_in_logs: bool | None = None
    visible_in_stats: bool | None = None
    filterable: bool | None = None
    groupable: bool | None = None


class UpdateParamDefinitionPayload(TransportPayload):
    key: str | None = None
    label: str | None = None
    param_type: str | None = None
    description: str | None = None
    overwrite_policy: str | None = None
    is_active: bool | None = None
    visible_in_logs: bool | None = None
    visible_in_stats: bool | None = None
    filterable: bool | None = None
    groupable: bool | None = None


class CreateSecretTemplatePayload(TransportPayload):
    app_id: int
    key: str
    name: str
    secret_type: str
    visibility: str


class UpdateSecretTemplatePayload(TransportPayload):
    key: str
    name: str
    secret_type: str
    visibility: str


class AppSecretValuePayload(TransportPayload):
    key: str
    value: str
    scope: str


class UpsertAppSecretsPayload(TransportPayload):
    platform_id: int | None = None
    secrets: list[AppSecretValuePayload] = Field(default_factory=list)


class UpdateAppSecretPayload(TransportPayload):
    value: str | None = None
    platform_id: int | None = None
    active_flag: bool | None = None
    version: float | None = None


class CreatePostbackRulePayload(TransportPayload):
    app_id: int
    platform_app_id: int | None = None
    name: str
    trigger_type: str
    event_key: str | None = None
    url: str
    http_method: str
    headers: JsonDict
    auth_params: JsonDict
    timeout: int
    retry_policy: JsonDict
    is_active: bool = False
    template: JsonDict = Field(default_factory=JsonDict)


class UpdatePostbackRulePayload(TransportPayload):
    platform_app_id: int | None = None
    name: str | None = None
    trigger_type: str | None = None
    event_key: str | None = None
    url: str | None = None
    http_method: str | None = None
    headers: JsonDict | None = None
    auth_params: JsonDict | None = None
    timeout: int | None = None
    retry_policy: JsonDict | None = None
    is_active: bool | None = None
    template: JsonDict | None = None


class CreatePushCampaignPayload(TransportPayload):
    app_id: int | None = None
    name: str
    title: str
    body: str 
    scheduled_at: str


class UpdatePushCampaignPayload(TransportPayload):
    name: str | None = None
    title: str | None = None
    body: str | None = None
    scheduled_at: str | None = None


class CreateRolePayload(TransportPayload):
    name: str 
    description: str | None = None
    permissions: list[str] = Field(default_factory=list)
    app_ids: list[int] = Field(default_factory=list)


class ShareAppPayload(TransportPayload):
    app_id: int
    manager_id: int
    role_code_slug: str


class StatsQueryPayload(TransportPayload):
    app_id: int | None = None
    platform: str | None = None
    group_by: str | None = None


class AuditLogQueryPayload(TransportPayload):
    app_id: int | None = None
    actor_id: int | None = None
    entity_type: str | None = None
    entity_id: int | None = None


class ClickLogsQueryPayload(TransportPayload):
    app_id: int | None = None
    click_id: str | None = None

class EventLogsQueryPayload(TransportPayload):
    app_id: int | None = None
    click_id: str | None = None
    event_key: str | None = None


class RolesQueryPayload(TransportPayload):
    app_id: int | None = None

