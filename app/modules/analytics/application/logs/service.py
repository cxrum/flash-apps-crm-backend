from app.modules.analytics.application.logs.contracts import (
    AnalyticsClickLog,
    AnalyticsEventLog,
    AnalyticsLogsPagination,
    ListAnalyticsClickLogsQuery,
    ListAnalyticsEventLogsQuery,
)
from app.modules.analytics.application.logs.mappers import AnalyticsLogsMapper
from app.modules.analytics.application.logs.protocol import AnalyticsLogsPort
from app.modules.analytics.domain.uow import AnalyticsUnitOfWorkFactoryProtocol
from app.modules.crm.domain.pagination import Pagination


class AnalyticsLogsService(AnalyticsLogsPort):
    def __init__(self, uow_factory: AnalyticsUnitOfWorkFactoryProtocol) -> None:
        self._uow_factory = uow_factory

    def list_clicks(self, query: ListAnalyticsClickLogsQuery) -> list[AnalyticsClickLog]:
        with self._uow_factory.create() as uow:
            clicks = uow.click_repo.list_by_app_id(
                query.app_id,
                click_id=query.click_id,
                pagination=self._pagination(query.pagination),
            )

        return [AnalyticsLogsMapper.click_log_from_domain(click) for click in clicks]

    def list_events(self, query: ListAnalyticsEventLogsQuery) -> list[AnalyticsEventLog]:
        with self._uow_factory.create() as uow:
            events = uow.event_repo.list_by_app_id(
                query.app_id,
                click_id=query.click_id,
                event_key=query.event_key,
                pagination=self._pagination(query.pagination),
            )

        return [AnalyticsLogsMapper.event_log_from_domain(event) for event in events]

    @staticmethod
    def _pagination(pagination: AnalyticsLogsPagination) -> Pagination:
        return Pagination(
            start_at=pagination.start_at,
            end_at=pagination.end_at,
            limit=pagination.limit,
            offset=pagination.offset,
        )
