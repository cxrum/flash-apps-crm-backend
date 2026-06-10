from typing import Protocol

from app.application.admin.push.commands import (
    CreatePushCampaignCommand,
    DeletePushCampaignCommand,
    GetPushCampaignCommand,
    ListPushCampaignsCommand,
    PushDeviceRegisterCommand,
    UpdatePushCampaignCommand,
)
from app.application.admin.push.responses import (
    CreatePushCampaignResponse,
    DeletePushCampaignResponse,
    GetPushCampaignResponse,
    ListPushCampaignResponse,
    RegisterDeviceResponse,
    UpdatePushCampaignResponse,
)


class PushServiceProtocol(Protocol):
    def create(self, command: CreatePushCampaignCommand) -> CreatePushCampaignResponse: ...
    def update(self, command: UpdatePushCampaignCommand) -> UpdatePushCampaignResponse: ...
    def delete(self, command: DeletePushCampaignCommand) -> DeletePushCampaignResponse: ...
    def list(self, command: ListPushCampaignsCommand) -> ListPushCampaignResponse: ...
    def get(self, command: GetPushCampaignCommand) -> GetPushCampaignResponse: ...
    def register_device(self, command: PushDeviceRegisterCommand) -> RegisterDeviceResponse: ...
