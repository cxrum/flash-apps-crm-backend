from datetime import UTC

from app.modules.analytics.application.logs.contracts import (
    AnalyticsClickLog,
    AnalyticsEventLog,
    AnalyticsLogsPagination,
    ListAnalyticsClickLogsQuery,
    ListAnalyticsEventLogsQuery,
)
from app.modules.analytics.application.logs.protocol import AnalyticsLogsPort
from app.modules.crm.application.admin.ingestion.analytics_logs_gateway import AnalyticsLogsGateway
from app.modules.crm.application.admin.ingestion.commands import ListClickLogsCommand, ListEventLogsCommand
from app.modules.crm.application.admin.ingestion.responses import (
    ClickLogResponseEntry,
    ListClickLogsResponse,
    ListRawEventsResponse,
    RawEventLogResponseEntry,
)


class CrmIngestionAnalyticsLogsAdapter(AnalyticsLogsGateway):
    """Translates CRM's driven port into Analytics' public logs port."""

    def __init__(self, analytics_logs: AnalyticsLogsPort) -> None:
        self._analytics_logs = analytics_logs

    def list_clicks(self, command: ListClickLogsCommand) -> ListClickLogsResponse:
        logs = self._analytics_logs.list_clicks(
            ListAnalyticsClickLogsQuery(
                app_id=command.app_id,
                click_id=command.click_id,
                pagination=self._pagination_from(command),
            )
        )
        return ListClickLogsResponse(clicks=[self._click_response(log) for log in logs])

    def list_raw_events(self, command: ListEventLogsCommand) -> ListRawEventsResponse:
        logs = self._analytics_logs.list_events(
            ListAnalyticsEventLogsQuery(
                app_id=command.app_id,
                click_id=command.click_id,
                event_key=command.event_key,
                pagination=self._pagination_from(command),
            )
        )
        return ListRawEventsResponse(events=[self._event_response(log) for log in logs])

    @staticmethod
    def _pagination_from(command: ListClickLogsCommand | ListEventLogsCommand) -> AnalyticsLogsPagination:
        return AnalyticsLogsPagination(
            start_at=command.start_at.astimezone(UTC) if command.start_at is not None else None,
            end_at=command.end_at.astimezone(UTC) if command.end_at is not None else None,
            limit=command.limit,
            offset=command.offset,
        )

    @staticmethod
    def _click_response(log: AnalyticsClickLog) -> ClickLogResponseEntry:
        return ClickLogResponseEntry(
            click_id=log.click_id,
            app_platform_id=log.app_platform_id,
            status=log.status,
            raw_query=dict(log.raw_query),
            ip_address=log.ip_address,
            user_agent=log.user_agent,
            referrer=log.referrer,
            source=log.source,
            redirect_target=log.redirect_target,
            normalized_params=dict(log.normalized_params),
            created_at=log.created_at,
        )

    @staticmethod
    def _event_response(log: AnalyticsEventLog) -> RawEventLogResponseEntry:
        return RawEventLogResponseEntry(
            event_id=log.event_id,
            click_id=log.click_id,
            event_type=log.event_type,
            event_key=log.event_key,
            event_time_utc=log.event_time_utc,
            app_user_id=log.app_user_id,
            amount=log.amount,
            currency=log.currency,
            amount_usd=log.amount_usd,
            payload=dict(log.payload),
            created_at=log.created_at,
        )
