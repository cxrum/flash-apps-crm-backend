from __future__ import annotations

from typing import Any

from pydantic import Field

from app.api.v1.transport import TransportPayload


class TrackingRedirectPayload(TransportPayload):
    app_code: str
    platform: str
    redirect_url: str | None = None
    idempotency_key: str | None = None
    ip: str | None = None
    user_agent: str | None = None
    params: dict[str, Any] = Field(default_factory=dict)
