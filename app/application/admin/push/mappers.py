from typing import Mapping

from app.application.admin.push.commands import CreatePushCampaignCommand, DeletePushCampaignCommand, GetPushCampaignCommand, ListPushCampaignsCommand, StartPushCampaignCommand, UpdatePushCampaignCommand
from app.application.admin.push.responses import PushResponseEntry
from app.core.utils.general_mapper import GeneralMapper
from app.domain.push_campaign import CrmPushCampaignEntity


class PushResponseMapper:
    
    @classmethod
    def list_push_campaigns_from_transport(cls, payload: Mapping[str, object]) -> ListPushCampaignsCommand:
        return GeneralMapper.command_payload_to_command(ListPushCampaignsCommand, payload)

    @classmethod
    def get_push_campaign_from_transport(cls, payload: Mapping[str, object]) -> GetPushCampaignCommand:
        return GeneralMapper.command_payload_to_command(GetPushCampaignCommand, payload)

    @classmethod
    def create_push_campaign_from_transport(cls, payload: Mapping[str, object]) -> CreatePushCampaignCommand:
        return GeneralMapper.command_payload_to_command(CreatePushCampaignCommand, payload)

    @classmethod
    def update_push_campaign_from_transport(cls, payload: Mapping[str, object]) -> UpdatePushCampaignCommand:
        return GeneralMapper.command_payload_to_command(UpdatePushCampaignCommand, payload)

    @classmethod
    def delete_push_campaign_from_transport(cls, payload: Mapping[str, object]) -> DeletePushCampaignCommand:
        return GeneralMapper.command_payload_to_command(DeletePushCampaignCommand, payload)

    @classmethod
    def start_push_campaign_from_transport(cls, payload: Mapping[str, object]) -> StartPushCampaignCommand:
        return GeneralMapper.command_payload_to_command(StartPushCampaignCommand, payload)
    
    
class PushCommandsMapper:
    
    @classmethod
    def push_campaign_domain_to_value(cls, domain: CrmPushCampaignEntity) -> PushResponseEntry:
        return PushResponseEntry.model_validate(domain)
    