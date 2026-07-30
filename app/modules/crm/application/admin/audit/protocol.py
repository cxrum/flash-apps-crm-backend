from typing import Protocol

from app.modules.crm.application.admin.audit.commands import (
    ListAuditLogCommand,
)
from app.modules.crm.application.admin.audit.responses import (
    ListAuditLogsResponse,
)


class AuditServiceProtocol(Protocol):
    def list_audit_logs(self, command: ListAuditLogCommand) -> ListAuditLogsResponse: ...
