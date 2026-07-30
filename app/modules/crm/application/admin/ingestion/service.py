from app.modules.crm.application.access_decorators import require_permission
from app.modules.crm.application.admin.crm_authorization.protocol import CrmAuthorizationServiceProtocol
from app.modules.crm.application.admin.ingestion.analytics_logs_gateway import AnalyticsLogsGateway
from app.modules.crm.application.admin.ingestion.commands import ListClickLogsCommand, ListEventLogsCommand
from app.modules.crm.application.admin.ingestion.protocol import IngestionDataServiceProtocol
from app.modules.crm.application.admin.ingestion.responses import ListClickLogsResponse, ListRawEventsResponse
from app.modules.crm.domain.permission.CrmPermissionEntity import CrmPermissionEntity
from app.modules.crm.domain.uow import UnitOfWorkFactoryProtocol


class IngestionDataService(IngestionDataServiceProtocol):
    def __init__(
        self,
        analytics_logs_gateway: AnalyticsLogsGateway,
        uow_factory: UnitOfWorkFactoryProtocol,
        authorization_service: CrmAuthorizationServiceProtocol,
    ) -> None:
        self._uow_factory = uow_factory
        self._authorization_service = authorization_service
        self._analytics_logs_gateway = analytics_logs_gateway

    @require_permission(CrmPermissionEntity.view_raw_logs_permission())
    def list_clicks(
        self,
        command: ListClickLogsCommand,
    ) -> ListClickLogsResponse:
        return self._analytics_logs_gateway.list_clicks(command)

    @require_permission(CrmPermissionEntity.view_raw_logs_permission())
    def list_raw_events(
        self,
        command: ListEventLogsCommand,
    ) -> ListRawEventsResponse:
        return self._analytics_logs_gateway.list_raw_events(command)
