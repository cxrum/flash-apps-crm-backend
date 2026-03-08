from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field
from dataclasses import dataclass


class DeviceCommand(BaseModel):
    os_version: str
    model: str
    language: str
    timezone: str


class IdsCommand(BaseModel):
    anonymous_id: str
    user_id: str | None = None


class AttributionCommand(BaseModel):
    click_id: str | None = None
    source: Literal["facebook", "google", "organic", "unknown"]
    campaign: str | None = None
    adset: str | None = None
    ad: str | None = None


class GeoCommand(BaseModel):
    country: str
    ip: str | None = None


class EventItemCommand(BaseModel):
    event_id: str
    event_name: str
    event_time: datetime
    platform: Literal["android", "ios"]
    app_version: str
    device: DeviceCommand
    ids: IdsCommand
    attribution: AttributionCommand
    geo: GeoCommand
    params: dict = Field(default_factory=dict)


class EventsBatchCommand(BaseModel):
    model_config = ConfigDict(extra="ignore")

    sdk_version: str
    sent_at: datetime
    events: list[EventItemCommand] = Field(min_length=1, max_length=500)


@dataclass(frozen=True)
class IngestEventsBatchCommand:
    app_id: int
    env: str
    signature: str
    payload: EventsBatchCommand
