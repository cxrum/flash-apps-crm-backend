from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Query, status
from pydantic import BaseModel

from app.api.v1.crm.payloads import (
    AppScopedListQueryPayload,
    AuditLogQueryPayload,
    ClickLogsQueryPayload,
    CreateAppPayload,
    CreateAppPlatformPayload,
    CreateConversionDefinitionPayload,
    CreateMetricDefinitionPayload,
    CreateParamDefinitionPayload,
    CreatePostbackRulePayload,
    CreatePushCampaignPayload,
    CreateRolePayload,
    CreateSecretTemplatePayload,
    EventLogsQueryPayload,
    OptionalAppScopedListQueryPayload,
    RolesQueryPayload,
    StatsQueryPayload,
    UpsertAppSecretsPayload,
)
from app.api.v1.stubs import build_stub_response
from app.api.v1.transport import PaginationQueryPayload
from app.application.admin.mappers import AdminCommandMapper

router = APIRouter()


def _payload_dict(payload: BaseModel, **extra: object) -> dict[str, Any]:
    data = payload.model_dump(exclude_none=True)
    data.update({key: value for key, value in extra.items() if value is not None})
    return data


@router.get("/apps", tags=["admin"])
async def list_apps(
    limit: int | None = Query(default=None, ge=1, le=1000),
    offset: int | None = Query(default=None, ge=0),
    search: str | None = Query(default=None),
) -> dict[str, Any]:
    payload = PaginationQueryPayload(limit=limit, offset=offset, search=search)
    command = AdminCommandMapper.list_apps_from_transport(_payload_dict(payload))
    return build_stub_response(command)


@router.post("/apps", status_code=status.HTTP_201_CREATED, tags=["admin"])
async def create_app(payload: CreateAppPayload) -> dict[str, Any]:
    command = AdminCommandMapper.create_app_from_transport(_payload_dict(payload))
    return build_stub_response(command)


@router.get("/apps/{app_id}/platforms", tags=["admin"])
async def list_app_platforms(
    app_id: int,
    limit: int | None = Query(default=None, ge=1, le=1000),
    offset: int | None = Query(default=None, ge=0),
    search: str | None = Query(default=None),
) -> dict[str, Any]:
    payload = AppScopedListQueryPayload(app_id=app_id, limit=limit, offset=offset, search=search)
    command = AdminCommandMapper.list_app_platforms_from_transport(_payload_dict(payload))
    return build_stub_response(command)


@router.post("/apps/{app_id}/platforms", status_code=status.HTTP_201_CREATED, tags=["admin"])
async def create_app_platform(app_id: int, payload: CreateAppPlatformPayload) -> dict[str, Any]:
    command = AdminCommandMapper.create_app_platform_from_transport(_payload_dict(payload, app_id=app_id))
    return build_stub_response(command)


@router.get("/metrics", tags=["admin"])
async def list_metrics(
    limit: int | None = Query(default=None, ge=1, le=1000),
    offset: int | None = Query(default=None, ge=0),
    search: str | None = Query(default=None),
) -> dict[str, Any]:
    payload = PaginationQueryPayload(limit=limit, offset=offset, search=search)
    command = AdminCommandMapper.list_metrics_from_transport(_payload_dict(payload))
    return build_stub_response(command)


@router.post("/metrics", status_code=status.HTTP_201_CREATED, tags=["admin"])
async def create_metric(payload: CreateMetricDefinitionPayload) -> dict[str, Any]:
    command = AdminCommandMapper.create_metric_from_transport(_payload_dict(payload))
    return build_stub_response(command)


@router.get("/conversions", tags=["admin"])
async def list_conversions(
    limit: int | None = Query(default=None, ge=1, le=1000),
    offset: int | None = Query(default=None, ge=0),
    search: str | None = Query(default=None),
) -> dict[str, Any]:
    payload = PaginationQueryPayload(limit=limit, offset=offset, search=search)
    command = AdminCommandMapper.list_conversions_from_transport(_payload_dict(payload))
    return build_stub_response(command)


@router.post("/conversions", status_code=status.HTTP_201_CREATED, tags=["admin"])
async def create_conversion(payload: CreateConversionDefinitionPayload) -> dict[str, Any]:
    command = AdminCommandMapper.create_conversion_from_transport(_payload_dict(payload))
    return build_stub_response(command)


@router.get("/params", tags=["admin"])
async def list_params(
    limit: int | None = Query(default=None, ge=1, le=1000),
    offset: int | None = Query(default=None, ge=0),
    search: str | None = Query(default=None),
) -> dict[str, Any]:
    payload = PaginationQueryPayload(limit=limit, offset=offset, search=search)
    command = AdminCommandMapper.list_params_from_transport(_payload_dict(payload))
    return build_stub_response(command)


@router.post("/params", status_code=status.HTTP_201_CREATED, tags=["admin"])
async def create_param(payload: CreateParamDefinitionPayload) -> dict[str, Any]:
    command = AdminCommandMapper.create_param_from_transport(_payload_dict(payload))
    return build_stub_response(command)


@router.get("/secrets/templates", tags=["admin"])
async def list_secret_templates(
    limit: int | None = Query(default=None, ge=1, le=1000),
    offset: int | None = Query(default=None, ge=0),
    search: str | None = Query(default=None),
) -> dict[str, Any]:
    payload = PaginationQueryPayload(limit=limit, offset=offset, search=search)
    command = AdminCommandMapper.list_secret_templates_from_transport(_payload_dict(payload))
    return build_stub_response(command)


@router.post("/secrets/templates", status_code=status.HTTP_201_CREATED, tags=["admin"])
async def create_secret_template(payload: CreateSecretTemplatePayload) -> dict[str, Any]:
    command = AdminCommandMapper.create_secret_template_from_transport(_payload_dict(payload))
    return build_stub_response(command)


@router.get("/apps/{app_id}/secrets", tags=["admin"])
async def list_app_secrets(
    app_id: int,
    limit: int | None = Query(default=None, ge=1, le=1000),
    offset: int | None = Query(default=None, ge=0),
    search: str | None = Query(default=None),
) -> dict[str, Any]:
    payload = AppScopedListQueryPayload(app_id=app_id, limit=limit, offset=offset, search=search)
    command = AdminCommandMapper.list_app_secrets_from_transport(_payload_dict(payload))
    return build_stub_response(command)


@router.post("/apps/{app_id}/secrets", status_code=status.HTTP_201_CREATED, tags=["admin"])
async def upsert_app_secrets(app_id: int, payload: UpsertAppSecretsPayload) -> dict[str, Any]:
    command = AdminCommandMapper.upsert_app_secrets_from_transport(_payload_dict(payload, app_id=app_id))
    return build_stub_response(command)


@router.get("/postbacks", tags=["admin"])
async def list_postbacks(
    app_id: int | None = Query(default=None),
    limit: int | None = Query(default=None, ge=1, le=1000),
    offset: int | None = Query(default=None, ge=0),
    search: str | None = Query(default=None),
) -> dict[str, Any]:
    payload = OptionalAppScopedListQueryPayload(app_id=app_id, limit=limit, offset=offset, search=search)
    command = AdminCommandMapper.list_postbacks_from_transport(_payload_dict(payload))
    return build_stub_response(command)


@router.post("/postbacks", status_code=status.HTTP_201_CREATED, tags=["admin"])
async def create_postback(payload: CreatePostbackRulePayload) -> dict[str, Any]:
    command = AdminCommandMapper.create_postback_from_transport(_payload_dict(payload))
    return build_stub_response(command)


@router.get("/push", tags=["admin"])
async def list_push_campaigns(
    app_id: int | None = Query(default=None),
    limit: int | None = Query(default=None, ge=1, le=1000),
    offset: int | None = Query(default=None, ge=0),
    search: str | None = Query(default=None),
) -> dict[str, Any]:
    payload = OptionalAppScopedListQueryPayload(app_id=app_id, limit=limit, offset=offset, search=search)
    command = AdminCommandMapper.list_push_campaigns_from_transport(_payload_dict(payload))
    return build_stub_response(command)


@router.post("/push", status_code=status.HTTP_201_CREATED, tags=["admin"])
async def create_push_campaign(payload: CreatePushCampaignPayload) -> dict[str, Any]:
    command = AdminCommandMapper.create_push_campaign_from_transport(_payload_dict(payload))
    return build_stub_response(command)


@router.get("/stats", tags=["admin"])
async def get_stats(
    app_id: int | None = Query(default=None),
    platform: str | None = Query(default=None),
    group_by: str | None = Query(default=None),
    start_at: str | None = Query(default=None),
    end_at: str | None = Query(default=None),
    limit: int | None = Query(default=None, ge=1, le=1000),
    offset: int | None = Query(default=None, ge=0),
    search: str | None = Query(default=None),
) -> dict[str, Any]:
    payload = StatsQueryPayload(
        app_id=app_id,
        platform=platform,
        group_by=group_by,
        start_at=start_at,
        end_at=end_at,
        limit=limit,
        offset=offset,
        search=search,
    )
    command = AdminCommandMapper.stats_from_transport(_payload_dict(payload))
    return build_stub_response(command)


@router.get("/logs/clicks", tags=["admin"])
async def list_click_logs(
    app_id: int | None = Query(default=None),
    click_id: str | None = Query(default=None),
    start_at: str | None = Query(default=None),
    end_at: str | None = Query(default=None),
    limit: int | None = Query(default=None, ge=1, le=1000),
    offset: int | None = Query(default=None, ge=0),
    search: str | None = Query(default=None),
) -> dict[str, Any]:
    payload = ClickLogsQueryPayload(
        app_id=app_id,
        click_id=click_id,
        start_at=start_at,
        end_at=end_at,
        limit=limit,
        offset=offset,
        search=search,
    )
    command = AdminCommandMapper.click_logs_from_transport(_payload_dict(payload))
    return build_stub_response(command)


@router.get("/logs/events", tags=["admin"])
async def list_event_logs(
    app_id: int | None = Query(default=None),
    click_id: str | None = Query(default=None),
    event_key: str | None = Query(default=None),
    start_at: str | None = Query(default=None),
    end_at: str | None = Query(default=None),
    limit: int | None = Query(default=None, ge=1, le=1000),
    offset: int | None = Query(default=None, ge=0),
    search: str | None = Query(default=None),
) -> dict[str, Any]:
    payload = EventLogsQueryPayload(
        app_id=app_id,
        click_id=click_id,
        event_key=event_key,
        start_at=start_at,
        end_at=end_at,
        limit=limit,
        offset=offset,
        search=search,
    )
    command = AdminCommandMapper.event_logs_from_transport(_payload_dict(payload))
    return build_stub_response(command)


@router.get("/roles", tags=["admin"])
async def list_roles(
    app_id: int | None = Query(default=None),
    limit: int | None = Query(default=None, ge=1, le=1000),
    offset: int | None = Query(default=None, ge=0),
    search: str | None = Query(default=None),
) -> dict[str, Any]:
    payload = RolesQueryPayload(app_id=app_id, limit=limit, offset=offset, search=search)
    command = AdminCommandMapper.list_roles_from_transport(_payload_dict(payload))
    return build_stub_response(command)


@router.post("/roles", status_code=status.HTTP_201_CREATED, tags=["admin"])
async def create_role(payload: CreateRolePayload) -> dict[str, Any]:
    command = AdminCommandMapper.create_role_from_transport(_payload_dict(payload))
    return build_stub_response(command)


@router.get("/audit", tags=["admin"])
async def get_audit_log(
    actor_id: int | None = Query(default=None),
    entity_type: str | None = Query(default=None),
    entity_id: int | None = Query(default=None),
    start_at: str | None = Query(default=None),
    end_at: str | None = Query(default=None),
    limit: int | None = Query(default=None, ge=1, le=1000),
    offset: int | None = Query(default=None, ge=0),
    search: str | None = Query(default=None),
) -> dict[str, Any]:
    payload = AuditLogQueryPayload(
        actor_id=actor_id,
        entity_type=entity_type,
        entity_id=entity_id,
        start_at=start_at,
        end_at=end_at,
        limit=limit,
        offset=offset,
        search=search,
    )
    command = AdminCommandMapper.audit_log_from_transport(_payload_dict(payload))
    return build_stub_response(command)
