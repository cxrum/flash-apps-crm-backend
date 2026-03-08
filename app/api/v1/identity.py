from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.application.identity.entities import LinkIdentityCommand
from app.application.identity.identity_usecases import IdentityUseCases
from app.di.dependencies import get_identity_usecases
from app.domain.identity.service import InvalidAnonymousIdError

router = APIRouter()


class IdentityLinkPayload(BaseModel):
    anonymous_id: str
    user_id: str
    linked_at: datetime


@router.post("", status_code=status.HTTP_201_CREATED, tags=["v1"])
def link_identity(
    payload: IdentityLinkPayload,
    identity_usecases: IdentityUseCases = Depends(get_identity_usecases),
) -> dict[str, str]:
    
    command = LinkIdentityCommand(
        anonymous_id=payload.anonymous_id,
        user_id=payload.user_id,
        linked_at=payload.linked_at,
    )
    
    try:
        result = identity_usecases.link_identity(command)
    except InvalidAnonymousIdError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return result.as_dict()
