from __future__ import annotations

from typing import Any

from pydantic import Field

from app.api.v1.transport import PaginationQueryPayload, TransportPayload


class CreateAppPayload(TransportPayload):
    code: str | None = None
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


class CreateAppPlatformPayload(TransportPayload):
    platform: str | None = None
    install_key: str | None = None
    is_active: bool | None = None


class CreateMetricDefinitionPayload(TransportPayload):
    key: str | None = None
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


class CreateConversionDefinitionPayload(TransportPayload):
    key: str | None = None
    name: str | None = None
    description: str | None = None
    currency: str | None = None
    is_active: bool | None = None


class CreateParamDefinitionPayload(TransportPayload):
    key: str | None = None
    label: str | None = None
    param_type: str | None = None
    is_required: bool | None = None


class CreateSecretTemplatePayload(TransportPayload):
    key: str | None = None
    name: str | None = None
    secret_type: str | None = None
    visibility: str | None = None


class AppSecretValuePayload(TransportPayload):
    key: str | None = None
    value: str | None = None
    scope: str | None = None


class UpsertAppSecretsPayload(TransportPayload):
    platform_id: int | None = None
    secrets: list[AppSecretValuePayload] = Field(default_factory=list)


class CreatePostbackRulePayload(TransportPayload):
    app_id: int | None = None
    name: str | None = None
    event_key: str | None = None
    url: str | None = None
    is_active: bool | None = None


class CreatePushCampaignPayload(TransportPayload):
    app_id: int | None = None
    name: str | None = None
    title: str | None = None
    body: str | None = None
    scheduled_at: str | None = None


class CreateRolePayload(TransportPayload):
    name: str | None = None
    description: str | None = None
    permissions: list[str] = Field(default_factory=list)
    app_ids: list[int] = Field(default_factory=list)


class AppScopedListQueryPayload(PaginationQueryPayload):
    app_id: int


class OptionalAppScopedListQueryPayload(PaginationQueryPayload):
    app_id: int | None = None


class StatsQueryPayload(PaginationQueryPayload):
    app_id: int | None = None
    platform: str | None = None
    group_by: str | None = None
    start_at: str | None = None
    end_at: str | None = None


class ClickLogsQueryPayload(PaginationQueryPayload):
    app_id: int | None = None
    click_id: str | None = None
    start_at: str | None = None
    end_at: str | None = None


class EventLogsQueryPayload(PaginationQueryPayload):
    app_id: int | None = None
    click_id: str | None = None
    event_key: str | None = None
    start_at: str | None = None
    end_at: str | None = None


class RolesQueryPayload(PaginationQueryPayload):
    app_id: int | None = None


class AuditLogQueryPayload(PaginationQueryPayload):
    actor_id: int | None = None
    entity_type: str | None = None
    entity_id: int | None = None
    start_at: str | None = None
    end_at: str | None = None


class RawPayload(TransportPayload):
    payload: dict[str, Any] = Field(default_factory=dict)
