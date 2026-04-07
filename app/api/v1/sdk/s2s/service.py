from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Body, Depends, Request, status

from app.core.utils.general_mapper import GeneralMapper
from app.api.v1.sdk.s2s.payloads import S2SClickPayload
from app.application.sdk.s2s.mappers import S2SCommandMapper
from app.application.sdk.s2s.service import ClickService
from app.di.services import get_s2s_service

router = APIRouter()


@router.post("/click", status_code=status.HTTP_202_ACCEPTED, tags=["s2s"])
async def ingest_s2s_click(
    request: Request,
    payload: Annotated[S2SClickPayload, Body()],
    s2s_service: ClickService = Depends(get_s2s_service),
) -> str:
    
    user_agent = request.headers.get("user-agent")
    
    command = S2SCommandMapper.click_from_transport(
        GeneralMapper.to_dict(
            payload, 
            ip=request.client.host if request.client is not None else None,
            user_agent=user_agent
        )
    )
    
    response = s2s_service.process_s2s_click(command)
    
    return response.model_dump_json()
