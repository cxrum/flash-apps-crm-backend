from typing import Protocol

from app.application.admin.logs.commands import (
    ListAuditLogCommand,
    ListClickLogsCommand,
    ListEventLogsCommand,
)
from app.application.admin.logs.responses import (
    ListAuditLogsResponse,
    ListClickLogsResponse,
    ListRawEventsResponse,
)


class LogsServiceProtocol(Protocol):
    def list_clicks(self, command: ListClickLogsCommand) -> ListClickLogsResponse: ...
    def list_raw_events(self, command: ListEventLogsCommand) -> ListRawEventsResponse: ...
    def list_audit_logs(self, command: ListAuditLogCommand) -> ListAuditLogsResponse: ...
