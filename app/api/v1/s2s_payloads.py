from __future__ import annotations

from typing import Any

from pydantic import Field

from app.api.v1.transport import TransportPayload


class S2SClickPayload(TransportPayload):
    app_code: str
    platform: str
    idempotency_key: str | None = None
    click_id: str | None = None
    redirect_url: str | None = None
    ip: str | None = None
    user_agent: str | None = None
    params: dict[str, Any] = Field(default_factory=dict)
