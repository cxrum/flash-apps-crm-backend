from __future__ import annotations

from pydantic import Field

from app.application.base import FlexibleCommand, JsonDict


class S2SClickCommand(FlexibleCommand):
    app_code: str
    platform: str
    signature: str
    idempotency_key: str | None = None
    click_id: str | None = None
    redirect_url: str | None = None
    ip: str | None = None
    user_agent: str | None = None
    params: JsonDict = Field(default_factory=dict)
    raw_params: str
