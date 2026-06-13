from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query, Request, status
from fastapi.responses import RedirectResponse

from app.modules.analytics.api.v1.tracking.payloads import TrackingRedirectQueries
from app.modules.crm.api.v1.stubs import build_stub_response
from app.modules.crm.application.sdk.s2s.protocol import ClickServiceProtocol
from app.modules.crm.application.tracking.mappers import TrackingCommandMapper
from app.modules.crm.core.utils.general_mapper import GeneralMapper as GeneralMapper
from app.modules.crm.di.services import get_s2s_service

router = APIRouter()


@router.get("/r/{app_code}/{platform}", tags=["tracking"])
async def tracking_redirect(
    request: Request,
    app_code: str,
    platform: str,
    redirect_url: Annotated[str, Query()],
    idempotency_key: Annotated[str | None, Query()] = None,
    s2s_service: ClickServiceProtocol = Depends(get_s2s_service),
) -> RedirectResponse:

    user_agent = request.headers.get("user-agent")

    command = TrackingCommandMapper.redirect_from_transport(
        GeneralMapper.to_dict(
            app_code=app_code,
            platform=platform,
            redirect_url=redirect_url,
            idempotency_key=idempotency_key,
            params=request.query_params,
            ip=request.client.host if request.client is not None else None,
            user_agent=user_agent,
        )
    )

    s2s_service.process_redirect_click(command)

    return RedirectResponse(url=redirect_url, status_code=status.HTTP_308_PERMANENT_REDIRECT)
