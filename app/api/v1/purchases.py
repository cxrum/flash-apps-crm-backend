from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, Header, HTTPException, status
from pydantic import BaseModel

from app.application.purchases.entities import VerifyPurchaseCommand
from app.application.purchases.purchase_usecases import PurchasesUseCases
from app.di.dependencies import get_purchases_usecases
from app.domain.purchases.service import AppNotFoundError, InvalidPlatformError, UserNotFoundError

router = APIRouter()


class PurchaseVerifyPayload(BaseModel):
    anonymous_id: str
    user_id: str
    linked_at: datetime


@router.post("/verify", status_code=status.HTTP_200_OK, tags=["v1"])
def verify_purchase(
    payload: PurchaseVerifyPayload,
    purchases_usecases: PurchasesUseCases = Depends(get_purchases_usecases),
    x_app_id: int = Header(alias="X-App-Id"),
    x_platform: str = Header(alias="X-Platform"),
) -> dict[str, str | int | float | None]:
    
    command = VerifyPurchaseCommand(
        app_id=x_app_id,
        platform=x_platform,
        anonymous_id=payload.anonymous_id,
        user_id=payload.user_id,
        linked_at=payload.linked_at,
    )
    
    try:
        result = purchases_usecases.verify_purchase(command)
    except InvalidPlatformError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except AppNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except UserNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    return result.as_dict()
