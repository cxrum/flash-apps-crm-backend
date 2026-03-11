from __future__ import annotations

from pydantic import Field

from app.application.base import FlexibleCommand, JsonDict


class TrackingRedirectCommand(FlexibleCommand):
    app_code: str
    platform: str
    redirect_url: str | None = None
    idempotency_key: str | None = None
    ip: str | None = None
    user_agent: str | None = None
    params: JsonDict = Field(default_factory=dict)
