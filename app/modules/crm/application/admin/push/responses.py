from datetime import datetime

from pydantic import Field

from app.modules.crm.application.base import BaseResponse, JsonDict


class PushResponseEntry(BaseResponse):
    campaign_id: int
    name: str
    title: str
    body: str
    status: str
    image_url: str | None = None
    target_link: str | None = None
    geo_filter: JsonDict = Field(default_factory=JsonDict)
    scheduled_at: datetime | None = None  # Convert to user local time


class CreatePushCampaignResponse(BaseResponse):
    campaign: PushResponseEntry


class UpdatePushCampaignResponse(BaseResponse):
    campaign: PushResponseEntry


class DeletePushCampaignResponse(BaseResponse):
    campaign: PushResponseEntry


class ListPushCampaignResponse(BaseResponse):
    campaigns: list[PushResponseEntry]


class GetPushCampaignResponse(BaseResponse):
    campaign: PushResponseEntry


class RegisterDeviceResponse(BaseResponse):
    pass
