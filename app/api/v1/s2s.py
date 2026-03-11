from __future__ import annotations

from typing import Any

from fastapi import APIRouter, status
from pydantic import BaseModel

from app.api.v1.s2s_payloads import S2SClickPayload
from app.api.v1.stubs import build_stub_response
from app.application.s2s.mappers import S2SCommandMapper

router = APIRouter()


def _dump_transport(payload: BaseModel) -> dict[str, Any]:
    return payload.model_dump(exclude_none=True)


@router.post("/click", status_code=status.HTTP_202_ACCEPTED, tags=["s2s"])
async def ingest_s2s_click(payload: S2SClickPayload) -> dict[str, Any]:
    command = S2SCommandMapper.click_from_transport(_dump_transport(payload))
    return build_stub_response(command)
