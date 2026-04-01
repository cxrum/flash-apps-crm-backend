from __future__ import annotations

from typing import Any

from pydantic import Field

from app.api.v1.transport import TransportPayload


class TrackingRedirectQueries(TransportPayload):
    app_code: str
    platform: str