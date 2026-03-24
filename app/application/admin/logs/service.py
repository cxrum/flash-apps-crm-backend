from app.application.admin.entities import (
    GetAuditLogCommand,
    ListClickLogsCommand,
    ListEventLogsCommand,
)
from app.application.admin.responses import (
    ListAuditLogsResponse,
    ListClickLogsResponse,
    ListRawEventsResponse,
)
from app.domain.uow import UnitOfWorkFactoryProtocol


class LogsService:
    def __init__(
        self,
        uow_factory: UnitOfWorkFactoryProtocol,
    ) -> None:
        self._uow_factory = uow_factory
        
        
    def list_clicks(
        self,
        command: ListClickLogsCommand,
    ) -> ListClickLogsResponse: ...

    def list_raw_events(
        self,
        command: ListEventLogsCommand,
    ) -> ListRawEventsResponse: ...

    def list_audit_logs(
        self,
        command: GetAuditLogCommand,
    ) -> ListAuditLogsResponse: ...
