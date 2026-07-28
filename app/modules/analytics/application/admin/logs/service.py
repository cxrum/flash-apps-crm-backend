from app.modules.analytics.application.admin.logs.protocol import AnalyticsLogsServiceProtocol
from app.modules.crm.application.access_decorators import require_permission
from app.modules.crm.application.admin.logs.commands import ListClickLogsCommand, ListEventLogsCommand
from app.modules.crm.application.admin.logs.mappers import LogsCommandsMapper
from app.modules.crm.application.admin.logs.responses import ListClickLogsResponse, ListRawEventsResponse
from app.modules.crm.application.mapper import PaginationMapper
from app.modules.crm.domain.permission.CrmPermissionEntity import CrmPermissionEntity
from app.modules.crm.domain.uow import UnitOfWorkFactoryProtocol


class AnalyticsLogsService(AnalyticsLogsServiceProtocol):
    def __init__(self, uow_factory: UnitOfWorkFactoryProtocol) -> None:
        self._uow_factory = uow_factory

    @require_permission(CrmPermissionEntity.view_raw_logs_permission())
    def list_clicks(self, command: ListClickLogsCommand) -> ListClickLogsResponse:
        with self._uow_factory.create() as uow:
            clicks = uow.click_repo.list_by_app_id(
                command.app_id,
                click_id=command.click_id,
                pagination=PaginationMapper.pagination_from_command(command),
            )

        return ListClickLogsResponse(clicks=[LogsCommandsMapper.click_log_domain_to_value(it) for it in clicks])

    @require_permission(CrmPermissionEntity.view_raw_logs_permission())
    def list_raw_events(self, command: ListEventLogsCommand) -> ListRawEventsResponse:
        with self._uow_factory.create() as uow:
            events = uow.event_repo.list_by_app_id(
                command.app_id,
                click_id=command.click_id,
                event_key=command.event_key,
                pagination=PaginationMapper.pagination_from_command(command),
            )

        return ListRawEventsResponse(events=[LogsCommandsMapper.event_log_domain_to_value(it) for it in events])
