from typing import Mapping

from app.application.admin.logs.commands import ListAuditLogCommand, ListClickLogsCommand, ListEventLogsCommand
from app.application.admin.logs.responses import AuditLogResponseEntry, ClickLogResponseEntry, RawEventLogResponseEntry
from app.core.utils.general_mapper import GeneralMapper
from app.domain.audit_log.CrmAuditLogEntity import CrmAuditLogEntity
from app.domain.click.CrmClickEntity import CrmClickEntity
from app.domain.events.CrmEventEntity import EventEntity


class LogsResponseMapper:
    @classmethod
    def audit_logs_from_transport(cls, payload: Mapping[str, object]) -> ListAuditLogCommand:
        return GeneralMapper.command_payload_to_command(ListAuditLogCommand, payload)

    @classmethod
    def click_logs_from_transport(cls, payload: Mapping[str, object]) -> ListClickLogsCommand:
        return GeneralMapper.command_payload_to_command(ListClickLogsCommand, payload)

    @classmethod
    def event_logs_from_transport(cls, payload: Mapping[str, object]) -> ListEventLogsCommand:
        return GeneralMapper.command_payload_to_command(ListEventLogsCommand, payload)
    
class LogsCommandsMapper:
    
    @classmethod
    def audit_log_domain_to_value(cls, domain: CrmAuditLogEntity) -> AuditLogResponseEntry:
        return AuditLogResponseEntry.model_validate(domain)
    
    @classmethod
    def click_log_domain_to_value(cls, domain: CrmClickEntity) -> ClickLogResponseEntry:
        return ClickLogResponseEntry.model_validate(domain)
    
    @classmethod
    def event_log_domain_to_value(cls, domain: EventEntity) -> RawEventLogResponseEntry:
        return RawEventLogResponseEntry.model_validate(domain)
    