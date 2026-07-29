from pydantic import Field

from app.modules.crm.application.base import FlexibleCommand, JsonDict, PaginationCommand


class PushDeviceValueCommand(FlexibleCommand):
    os_name: str | None = None
    os_version: str | None = None
    device_brand: str | None = None
    device_model: str | None = None
    app_version: str | None = None
    sdk_version: str | None = None


class ListPushCampaignsCommand(PaginationCommand):
    crm_user_id: int
    app_id: int


class GetPushCampaignCommand(FlexibleCommand):
    crm_user_id: int
    push_id: int
    app_id: int


class CreatePushCampaignCommand(FlexibleCommand):
    crm_user_id: int
    app_id: int
    name: str
    title: str
    body: str
    image_url: str | None = None
    target_link: str | None = None
    geo_filter: JsonDict = Field(default_factory=JsonDict)
    status: str | None = None
    scheduled_at: str | None = None  # date time ISO 8601 Local with Offset


class UpdatePushCampaignCommand(FlexibleCommand):
    crm_user_id: int
    app_id: int
    campaign_id: int
    name: str | None = None
    title: str | None = None
    body: str | None = None
    image_url: str | None = None
    target_link: str | None = None
    geo_filter: JsonDict | None = None
    status: str | None = None
    scheduled_at: str | None = None  # date time ISO 8601 Local with Offset


class DeletePushCampaignCommand(FlexibleCommand):
    crm_user_id: int
    push_id: int


class StartPushCampaignCommand(FlexibleCommand):
    crm_user_id: int
    push_id: int
    app_id: int | None = None


class PushDeviceRegisterCommand(FlexibleCommand):
    install_key: str
    push_token: str
    click_id: str
    app_user_id: int | None = None
    provider: str | None = None
    device: PushDeviceValueCommand | None = None
    params: JsonDict = Field(default_factory=dict)
