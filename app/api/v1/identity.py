from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.domain.identity.dependencies import get_identity_service
from app.domain.identity.service import InvalidAnonymousIdError
from app.domain.identity.service_protocol import IdentityServiceProtocol

router = APIRouter()


class IdentityLinkPayload(BaseModel):
    anonymous_id: str
    user_id: str
    linked_at: datetime


@router.post("", status_code=status.HTTP_201_CREATED, tags=["v1"])
def link_identity(
    payload: IdentityLinkPayload,
    identity_service: IdentityServiceProtocol = Depends(get_identity_service),
) -> dict[str, str]:
    try:
        result = identity_service.link_identity(
            anonymous_id=payload.anonymous_id,
            user_id=payload.user_id,
            linked_at=payload.linked_at,
        )
    except InvalidAnonymousIdError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return result.as_dict()
