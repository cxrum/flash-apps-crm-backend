from collections.abc import Mapping

from app.core.utils.general_mapper import GeneralMapper
from app.modules.crm.application.admin.audit.commands import (
    ListAuditLogCommand,
)
from app.modules.crm.application.admin.audit.responses import (
    AuditLogResponseEntry,
)
from app.modules.crm.domain.audit_log.CrmAuditLogEntity import CrmAuditLogEntity


class AuditResponseMapper:
    @classmethod
    def audit_logs_from_transport(cls, payload: Mapping[str, object]) -> ListAuditLogCommand:
        return GeneralMapper.command_payload_to_command(ListAuditLogCommand, payload)


class AuditCommandsMapper:
    @classmethod
    def audit_log_domain_to_value(cls, domain: CrmAuditLogEntity) -> AuditLogResponseEntry:
        return AuditLogResponseEntry.model_validate(domain)
