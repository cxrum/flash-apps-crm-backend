from typing import Protocol

from app.modules.analytics.application.logs.contracts import (
    AnalyticsClickLog,
    AnalyticsEventLog,
    ListAnalyticsClickLogsQuery,
    ListAnalyticsEventLogsQuery,
)


class AnalyticsLogsPort(Protocol):
    def list_clicks(self, query: ListAnalyticsClickLogsQuery) -> list[AnalyticsClickLog]: ...
    def list_events(self, query: ListAnalyticsEventLogsQuery) -> list[AnalyticsEventLog]: ...
