from __future__ import annotations

import hmac
import threading
import time
from collections import defaultdict, deque
from datetime import datetime
from hashlib import sha256
from typing import Literal

from fastapi import APIRouter, Depends, Header, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ConfigDict, Field, ValidationError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.domain.events.service import DomainAppNotFoundError, EventsDomainService
from app.infra.db.repositories.events_repository import EventsRepository
from app.infra.db.session import get_db

router = APIRouter()

_RATE_LIMIT_WINDOW_SECONDS = 60
_rate_limit_hits: dict[tuple[int, str], deque[float]] = defaultdict(deque)
_rate_limit_lock = threading.Lock()


class DevicePayload(BaseModel):
    os_version: str
    model: str
    language: str
    timezone: str


class IdsPayload(BaseModel):
    anonymous_id: str
    user_id: str | None = None


class AttributionPayload(BaseModel):
    click_id: str | None = None
    source: Literal["facebook", "google", "organic", "unknown"]
    campaign: str | None = None
    adset: str | None = None
    ad: str | None = None


class GeoPayload(BaseModel):
    country: str
    ip: str | None = None


class EventItemPayload(BaseModel):
    event_id: str
    event_name: str
    event_time: datetime
    platform: Literal["android", "ios"]
    app_version: str
    device: DevicePayload
    ids: IdsPayload
    attribution: AttributionPayload
    geo: GeoPayload
    params: dict = Field(default_factory=dict)


class EventsBatchPayload(BaseModel):
    model_config = ConfigDict(extra="ignore")

    sdk_version: str
    sent_at: datetime
    events: list[EventItemPayload] = Field(min_length=1, max_length=500)


def get_events_repository(db: Session = Depends(get_db)) -> EventsRepository:
    return EventsRepository(db)


def get_events_domain_service(
    repository: EventsRepository = Depends(get_events_repository),
) -> EventsDomainService:
    return EventsDomainService(repository)


def _is_rate_limited(app_id: int, ip: str) -> bool:
    key = (app_id, ip)
    now = time.time()
    with _rate_limit_lock:
        bucket = _rate_limit_hits[key]
        while bucket and now - bucket[0] > _RATE_LIMIT_WINDOW_SECONDS:
            bucket.popleft()
        if len(bucket) >= settings.batch_rate_limit_per_minute:
            return True
        bucket.append(now)
    return False


def _verify_signature(raw_body: bytes, signature_header: str) -> bool:
    received = signature_header.strip()
    if received.lower().startswith("sha256="):
        received = received.split("=", 1)[1]
    expected = hmac.new(settings.app_secret.encode("utf-8"), raw_body, sha256).hexdigest()
    return hmac.compare_digest(expected, received)


@router.post("/batch", status_code=status.HTTP_202_ACCEPTED, tags=["v1"])
async def ingest_events_batch(
    request: Request,
    domain_service: EventsDomainService = Depends(get_events_domain_service),
    x_app_id: int = Header(alias="X-App-Id"),
    x_env: str = Header(alias="X-Env"),
    x_signature: str = Header(alias="X-Signature"),
) -> dict[str, int | str]:
    if x_env not in {"prod", "stage"}:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid X-Env header")

    request_ip = request.client.host if request.client else "unknown"
    if _is_rate_limited(app_id=x_app_id, ip=request_ip):
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate limit exceeded")

    raw_body = await request.body()
    if not _verify_signature(raw_body, x_signature):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid signature")

    try:
        payload = EventsBatchPayload.model_validate_json(raw_body)
    except ValidationError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=jsonable_encoder(exc.errors())) from exc

    try:
        result = domain_service.process_batch(
            app_id=x_app_id,
            environment=x_env,
            batch_payload=payload.model_dump(mode="python"),
        )
    except DomainAppNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    return result.as_dict()
