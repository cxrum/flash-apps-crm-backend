from app.application.base import FlexibleCommand, PaginationCommand


class ListPushCampaignsCommand(PaginationCommand):
    crm_user_id: int
    app_id: int | None = None


class GetPushCampaignCommand(FlexibleCommand):
    crm_user_id: int
    push_id: int
    app_id: int | None = None


class CreatePushCampaignCommand(FlexibleCommand):
    crm_user_id: int
    app_id: int | None = None
    name: str | None = None
    title: str | None = None
    body: str | None = None
    scheduled_at: str | None = None


class UpdatePushCampaignCommand(FlexibleCommand):
    crm_user_id: int
    push_id: int
    app_id: int | None = None
    name: str | None = None
    title: str | None = None
    body: str | None = None
    scheduled_at: str | None = None


class DeletePushCampaignCommand(FlexibleCommand):
    crm_user_id: int
    push_id: int
    app_id: int | None = None


class StartPushCampaignCommand(FlexibleCommand):
    crm_user_id: int
    push_id: int
    app_id: int | None = None