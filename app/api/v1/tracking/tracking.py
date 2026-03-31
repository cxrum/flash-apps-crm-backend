from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Query, Request

from app.core.utils.general_mapper import GeneralMapper as GeneralMapper
from app.api.v1.stubs import build_stub_response
from app.api.v1.tracking.payloads import TrackingRedirectPayload
from app.application.tracking.mappers import TrackingCommandMapper

router = APIRouter()


def _query_params(request: Request) -> dict[str, str]:
    ignored_keys = {"redirect_url", "idempotency_key"}
    return {key: value for key, value in request.query_params.items() if key not in ignored_keys}


@router.get("/r/{app_code}/{platform}", tags=["tracking"])
async def tracking_redirect(
    request: Request,
    app_code: str,
    platform: str,
    redirect_url: str | None = Query(default=None),
    idempotency_key: str | None = Query(default=None),
) -> dict[str, Any]:
    payload = TrackingRedirectPayload(
        app_code=app_code,
        platform=platform,
        redirect_url=redirect_url,
        idempotency_key=idempotency_key,
        ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
        params=_query_params(request),
    )
    command = TrackingCommandMapper.redirect_from_transport(GeneralMapper.to_dict(payload))
    return build_stub_response(command)
