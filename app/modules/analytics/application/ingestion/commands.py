from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import Field

from app.modules.crm.application.base import FlexibleCommand, JsonDict


class SdkDeviceValueCommand(FlexibleCommand):
    os_name: str | None = None
    os_version: str | None = None
    device_brand: str | None = None
    device_model: str | None = None
    app_version: str | None = None
    sdk_version: str | None = None


class SdkInstallCommand(FlexibleCommand):
    idempotency_key: str
    install_key: str
    click_id: str | None = None
    params: JsonDict = Field(default_factory=dict)
    device: SdkDeviceValueCommand


class SdkEventCommand(FlexibleCommand):
    idempotency_key: str
    type: Literal["metric", "conversion"]
    key: str
    event_time: datetime | None = None
    amount: float | None = None
    currency: str | None = None
    params: JsonDict = Field(default_factory=dict)


class SdkEventsCommand(FlexibleCommand):
    idempotency_key: str
    install_key: str
    click_id: str
    events: list[SdkEventCommand] = Field(min_length=1)


class SdkParamsUpdateCommand(FlexibleCommand):
    click_id: str
    idempotency_key: str
    params: JsonDict = Field(default_factory=dict)
    event_time: datetime | None = None


class SdkPushStartCommand(FlexibleCommand):
    click_id: str
    platfrom_id: int
