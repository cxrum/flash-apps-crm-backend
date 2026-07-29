from app.modules.analytics.application.admin.logs.protocol import AnalyticsLogsPort
from app.modules.analytics.application.admin.logs.mappers import AnalyticsLogsCommandsMapper
from app.modules.analytics.domain.uow import AnalyticsUnitOfWorkFactoryProtocol
from app.modules.crm.application.admin.logs.commands import ListClickLogsCommand, ListEventLogsCommand
from app.modules.crm.application.admin.logs.responses import ListClickLogsResponse, ListRawEventsResponse
from app.modules.crm.application.mapper import PaginationMapper


class AnalyticsLogsService(AnalyticsLogsPort):
    def __init__(self, uow_factory: AnalyticsUnitOfWorkFactoryProtocol) -> None:
        self._uow_factory = uow_factory

    def list_clicks(self, command: ListClickLogsCommand) -> ListClickLogsResponse:
        with self._uow_factory.create() as uow:
            clicks = uow.click_repo.list_by_app_id(
                command.app_id,
                click_id=command.click_id,
                pagination=PaginationMapper.pagination_from_command(command),
            )

        return ListClickLogsResponse(clicks=[AnalyticsLogsCommandsMapper.click_log_domain_to_value(it) for it in clicks])

    def list_raw_events(self, command: ListEventLogsCommand) -> ListRawEventsResponse:
        with self._uow_factory.create() as uow:
            events = uow.event_repo.list_by_app_id(
                command.app_id,
                click_id=command.click_id,
                event_key=command.event_key,
                pagination=PaginationMapper.pagination_from_command(command),
            )

        return ListRawEventsResponse(events=[AnalyticsLogsCommandsMapper.event_log_domain_to_value(it) for it in events])
