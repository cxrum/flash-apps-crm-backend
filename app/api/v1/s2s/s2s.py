from __future__ import annotations

from typing import Any

from fastapi import APIRouter, status
from pydantic import BaseModel

from app.core.utils.general_mapper import GeneralMapper as GeneralMapper
from app.api.v1.s2s.payloads import S2SClickPayload
from app.api.v1.stubs import build_stub_response
from app.application.s2s.mappers import S2SCommandMapper

router = APIRouter()


@router.post("/click", status_code=status.HTTP_202_ACCEPTED, tags=["s2s"])
async def ingest_s2s_click(
    payload: S2SClickPayload
) -> dict[str, Any]:
    command = S2SCommandMapper.click_from_transport(GeneralMapper.to_dict(payload))
    return build_stub_response(command)
