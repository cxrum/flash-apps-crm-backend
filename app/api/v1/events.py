from __future__ import annotations

import threading
import time
from collections import defaultdict, deque

from fastapi import APIRouter, Depends, Header, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError

from app.application.events.entities import EventsBatchCommand
from app.application.events.event_usecases import EventUseCases, InvalidSignatureException
from app.application.events.mappers import IngestEventsBatchCommandMapper
from app.core.signature import SignatueVerifirer
from app.di.dependencies import get_event_usecases
from app.core.config import settings
from app.domain.events.service import DomainAppNotFoundError

router = APIRouter()

_rate_limit_hits: dict[tuple[int, str], deque[float]] = defaultdict(deque)
_rate_limit_lock = threading.Lock()


def _is_rate_limited(app_id: int, ip: str) -> bool:
    key = (app_id, ip)
    now = time.time()
    with _rate_limit_lock:
        bucket = _rate_limit_hits[key]
        while bucket and now - bucket[0] > settings.rate_limit_window_seconds:
            bucket.popleft()
        if len(bucket) >= settings.batch_rate_limit_per_window:
            return True
        bucket.append(now)
    return False


@router.post("/batch", status_code=status.HTTP_202_ACCEPTED, tags=["v1"])
async def ingest_events_batch(
    request: Request,
    use_cases: EventUseCases = Depends(get_event_usecases),
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
    if not SignatueVerifirer.verify_signature(raw_body, x_signature):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid signature")
        
    try:
        payload = EventsBatchCommand.model_validate_json(raw_body)
    except ValidationError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=jsonable_encoder(exc.errors())) from exc
    
    command = IngestEventsBatchCommandMapper.from_transport(
        app_id=x_app_id,
        env=x_env,
        signature=x_signature,
        payload=payload,
    )

    try:
        result = use_cases.process_batch(command)
        
    except DomainAppNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except InvalidSignatureException as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid signature")

    return result.as_dict()
