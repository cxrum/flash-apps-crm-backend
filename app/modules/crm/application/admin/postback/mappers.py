from typing import Mapping

from app.modules.crm.application.admin.postback.commands import (
    CreatePostbackRuleCommand,
    DeletePostbackRuleCommand,
    GetPostbackRuleCommand,
    ListPostbackRulesCommand,
    UpdatePostbackRuleCommand,
)
from app.modules.crm.application.admin.postback.responses import PostbackResponseEntry
from app.modules.crm.core.utils.general_mapper import GeneralMapper
from app.modules.crm.domain.postback_rule.CrmPostbackRuleEntity import CrmPostbackRuleEntity


class PostbackResponseMapper:
    @classmethod
    def list_postbacks_from_transport(cls, payload: Mapping[str, object]) -> ListPostbackRulesCommand:
        return GeneralMapper.command_payload_to_command(ListPostbackRulesCommand, payload)

    @classmethod
    def get_postback_from_transport(cls, payload: Mapping[str, object]) -> GetPostbackRuleCommand:
        return GeneralMapper.command_payload_to_command(GetPostbackRuleCommand, payload)

    @classmethod
    def create_postback_from_transport(cls, payload: Mapping[str, object]) -> CreatePostbackRuleCommand:
        return GeneralMapper.command_payload_to_command(CreatePostbackRuleCommand, payload)

    @classmethod
    def update_postback_from_transport(cls, payload: Mapping[str, object]) -> UpdatePostbackRuleCommand:
        return GeneralMapper.command_payload_to_command(UpdatePostbackRuleCommand, payload)

    @classmethod
    def delete_postback_from_transport(cls, payload: Mapping[str, object]) -> DeletePostbackRuleCommand:
        return GeneralMapper.command_payload_to_command(DeletePostbackRuleCommand, payload)


class PostbackCommandsMapper:
    @classmethod
    def postback_domain_to_value(cls, domain: CrmPostbackRuleEntity) -> PostbackResponseEntry:
        return PostbackResponseEntry(
            postback_id=domain.rule_id or 0,
            platform_app_id=domain.platform_app_id,
            name=domain.name,
            endpoint_url=domain.endpoint_url,
            trigger_type=domain.trigger_type,
            http_method=domain.http_method,
            headers=dict(domain.headers),
            auth_params=dict(domain.auth_params),
            template=dict(domain.template.items()),
            retry_policy=dict(domain.retry_policy),
            timeout=domain.timeout,
            is_active=domain.is_active,
            event_key=domain.event_key,
            created_at=domain.created_at,
            updated_at=domain.updated_at,
        )
