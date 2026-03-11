from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Query, status
from pydantic import BaseModel

from app.api.v1.sdk.payloads import (
    SdkConfigQueryPayload,
    SdkEventsPayload,
    SdkInstallPayload,
    SdkParamsUpdatePayload,
    SdkPushRegisterPayload,
)
from app.api.v1.stubs import build_stub_response
from app.application.sdk.mappers import SdkCommandMapper

router = APIRouter()


def _dump_transport(payload: BaseModel) -> dict[str, Any]:
    return payload.model_dump(exclude_none=True)


@router.post("/install", status_code=status.HTTP_202_ACCEPTED, tags=["sdk"])
async def create_or_link_install(payload: SdkInstallPayload) -> dict[str, Any]:
    command = SdkCommandMapper.install_from_transport(_dump_transport(payload))
    return build_stub_response(command)


@router.post("/events", status_code=status.HTTP_202_ACCEPTED, tags=["sdk"])
async def ingest_sdk_events(payload: SdkEventsPayload) -> dict[str, Any]:
    command = SdkCommandMapper.events_from_transport(_dump_transport(payload))
    return build_stub_response(command)


@router.post("/params/update", status_code=status.HTTP_202_ACCEPTED, tags=["sdk"])
async def update_sdk_params(payload: SdkParamsUpdatePayload) -> dict[str, Any]:
    command = SdkCommandMapper.params_update_from_transport(_dump_transport(payload))
    return build_stub_response(command)


@router.post("/push/register", status_code=status.HTTP_202_ACCEPTED, tags=["sdk"])
async def register_push_token(payload: SdkPushRegisterPayload) -> dict[str, Any]:
    command = SdkCommandMapper.push_register_from_transport(_dump_transport(payload))
    return build_stub_response(command)


@router.get("/config", tags=["sdk"])
async def get_public_config(
    install_key: str | None = Query(default=None),
    app_code: str | None = Query(default=None),
    platform: str | None = Query(default=None),
    crm_user_id: str | None = Query(default=None),
) -> dict[str, Any]:
    payload = SdkConfigQueryPayload(
        install_key=install_key,
        app_code=app_code,
        platform=platform,
        crm_user_id=crm_user_id,
    )
    command = SdkCommandMapper.config_from_transport(_dump_transport(payload))
    return build_stub_response(command)
