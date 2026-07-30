from typing import Protocol

from app.modules.analytics.application.attribution.contracts import AnalyticsClickContext, AnalyticsPostbackContext


class AnalyticsAttributionPort(Protocol):
    def get_click_context(self, click_id: str) -> AnalyticsClickContext | None: ...
    def get_postback_context(self, event_id: str) -> AnalyticsPostbackContext | None: ...
