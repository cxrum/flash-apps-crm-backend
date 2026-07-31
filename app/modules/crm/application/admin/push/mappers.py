from typing import Mapping

from app.core.utils.general_mapper import GeneralMapper
from app.modules.crm.application.admin.push.commands import (
    CreatePushCampaignCommand,
    DeletePushCampaignCommand,
    GetPushCampaignCommand,
    ListPushCampaignsCommand,
    PushDeviceRegisterCommand,
    StartPushCampaignCommand,
    UpdatePushCampaignCommand,
)
from app.modules.crm.application.admin.push.responses import PushResponseEntry
from app.modules.crm.domain.push_campaign import CrmPushCampaignEntity


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

    @classmethod
    def push_register_from_transport(cls, payload: Mapping[str, object]) -> PushDeviceRegisterCommand:
        return GeneralMapper.command_payload_to_command(PushDeviceRegisterCommand, payload)


class PushCommandsMapper:
    @classmethod
    def push_campaign_domain_to_value(cls, domain: CrmPushCampaignEntity) -> PushResponseEntry:
        return PushResponseEntry(
            campaign_id=domain.campaign_id or 0,
            name=domain.title,
            title=domain.title,
            body=domain.body,
            status=domain.status,
            image_url=domain.image_url,
            target_link=domain.target_link,
            geo_filter=dict(domain.geo_filter),
            scheduled_at=domain.scheduled_at,
        )
