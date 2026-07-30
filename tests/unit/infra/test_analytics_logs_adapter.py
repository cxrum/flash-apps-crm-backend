from datetime import UTC, datetime

from app.infra.analytics_logs_adapter import CrmIngestionAnalyticsLogsAdapter
from app.modules.analytics.application.logs.contracts import AnalyticsClickLog, AnalyticsEventLog
from app.modules.crm.application.admin.ingestion.commands import ListClickLogsCommand, ListEventLogsCommand


class _AnalyticsLogsPortStub:
    def __init__(self) -> None:
        self.click_query = None
        self.event_query = None

    def list_clicks(self, query):
        self.click_query = query
        return [
            AnalyticsClickLog(
                click_id="click-1",
                app_platform_id=3,
                status="accepted",
                raw_query={"campaign": "spring"},
                ip_address="127.0.0.1",
                user_agent="test-agent",
                referrer=None,
                source="sdk",
                redirect_target=None,
                normalized_params={"campaign": "spring"},
                created_at=None,
            )
        ]

    def list_events(self, query):
        self.event_query = query
        return [
            AnalyticsEventLog(
                event_id="event-1",
                click_id="click-1",
                event_type="conversion",
                event_key="purchase",
                event_time_utc=datetime(2026, 7, 30, tzinfo=UTC),
                app_user_id=5,
                amount=10.0,
                currency="USD",
                amount_usd=10.0,
                payload={"order_id": "order-1"},
                created_at=None,
            )
        ]


def test_adapter_translates_crm_click_requests_and_analytics_log_values() -> None:
    analytics_port = _AnalyticsLogsPortStub()
    adapter = CrmIngestionAnalyticsLogsAdapter(analytics_port)  # type: ignore[arg-type]

    response = adapter.list_clicks(ListClickLogsCommand(crm_user_id=7, app_id=11, click_id="click-1"))

    assert analytics_port.click_query.app_id == 11
    assert analytics_port.click_query.click_id == "click-1"
    assert response.clicks[0].click_id == "click-1"
    assert response.clicks[0].normalized_params == {"campaign": "spring"}


def test_adapter_translates_crm_event_requests_and_analytics_log_values() -> None:
    analytics_port = _AnalyticsLogsPortStub()
    adapter = CrmIngestionAnalyticsLogsAdapter(analytics_port)  # type: ignore[arg-type]

    response = adapter.list_raw_events(
        ListEventLogsCommand(crm_user_id=7, app_id=11, click_id="click-1", event_key="purchase")
    )

    assert analytics_port.event_query.app_id == 11
    assert analytics_port.event_query.event_key == "purchase"
    assert response.events[0].event_id == "event-1"
    assert response.events[0].payload == {"order_id": "order-1"}
