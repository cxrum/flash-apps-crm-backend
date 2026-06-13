from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import Field

from app.modules.crm.api.v1.transport import TransportPayload


class SdkDevicePayload(TransportPayload):
    os_name: str | None = None
    os_version: str | None = None
    device_brand: str | None = None
    device_model: str | None = None
    app_version: str | None = None
    sdk_version: str | None = None


class SdkInstallPayload(TransportPayload):
    install_key: str
    click_id: str | None = None
    params: dict[str, Any] = Field(default_factory=dict)
    device: SdkDevicePayload


class SdkEventPayload(TransportPayload):
    type: Literal["metric", "conversion"]
    key: str
    event_time: datetime | None = None  # date time ISO 8601 Local with Offset
    amount: float | None = None
    currency: str | None = None
    params: dict[str, Any] = Field(default_factory=dict)


class SdkEventsPayload(TransportPayload):
    install_key: str
    click_id: str
    events: list[SdkEventPayload] = Field(min_length=1)


class SdkParamsUpdatePayload(TransportPayload):
    click_id: str
    params: dict[str, Any] = Field(default_factory=dict)
    event_time: datetime | None = None  # date time ISO 8601 Local with Offset


class SdkPushRegisterPayload(TransportPayload):
    install_key: str
    token: str
    provider: str | None = None
    click_id: str | None = None
    crm_user_id: str | None = None
    device: SdkDevicePayload | None = None
    params: dict[str, Any] = Field(default_factory=dict)


class SdkConfigQueryPayload(TransportPayload):
    install_key: str | None = None
    app_code: str | None = None
    platform: str | None = None
