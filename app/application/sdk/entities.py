from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import Field

from app.application.base import FlexibleCommand, JsonDict


class SdkDeviceCommand(FlexibleCommand):
    os_name: str | None = None
    os_version: str | None = None
    device_brand: str | None = None
    device_model: str | None = None
    app_version: str | None = None
    sdk_version: str | None = None


class SdkInstallCommand(FlexibleCommand):
    install_key: str
    idempotency_key: str
    click_id: str | None = None
    params: JsonDict = Field(default_factory=dict)
    device: SdkDeviceCommand


class SdkEventCommand(FlexibleCommand):
    type: Literal["metric", "conversion"]
    key: str
    event_time: datetime | None = None
    amount: float | None = None
    currency: str | None = None
    params: JsonDict = Field(default_factory=dict)


class SdkEventsCommand(FlexibleCommand):
    install_key: str
    click_id: str
    idempotency_key: str
    events: list[SdkEventCommand] = Field(min_length=1)


class SdkParamsUpdateCommand(FlexibleCommand):
    click_id: str
    idempotency_key: str
    params: JsonDict = Field(default_factory=dict)
    event_time: datetime | None = None


class SdkPushRegisterCommand(FlexibleCommand):
    install_key: str
    token: str
    provider: str | None = None
    click_id: str | None = None
    crm_user_id: str | None = None
    idempotency_key: str | None = None
    device: SdkDeviceCommand | None = None
    params: JsonDict = Field(default_factory=dict)


class GetSdkConfigCommand(FlexibleCommand):
    install_key: str | None = None
    app_code: str | None = None
    platform: str | None = None
    crm_user_id: str | None = None

class SdkCreateAppCommand(FlexibleCommand):
    id: int
    name: str
    code_slug: str
    screanshots: dict
    logo_ur: str | None = None
    tech_description: str | None = None
    description: str | None = None

class SdkCreateAppPlatformCommand(FlexibleCommand):
    app_id: int
    platform: str
    package_name: str
    install_key: str
    store_url: str | None = None
    sdk_public_key: str | None = None
    sdk_secret_hash: str | None = None
    status: str = "active"
    platform_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    
    
class SdkApplicationConfigurationCommand(FlexibleCommand):
    app_id: int
    platform: str