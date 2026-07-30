from datetime import UTC, datetime, timedelta, timezone

from app.infra.analytics_logs_adapter import CrmIngestionAnalyticsLogsAdapter
from app.modules.analytics.application.logs.contracts import AnalyticsClickLog, AnalyticsEventLog
from app.modules.crm.application.admin.ingestion.commands import ListClickLogsCommand, ListEventLogsCommand
from app.modules.crm.application.admin.ingestion.service import IngestionDataService
from app.modules.crm.domain.permission.CrmPermissionEntity import CrmPermissionEntity
from tests.unit.doubles.domain.uow import StubUnitOfWork, StubUoWFactory


class _AnalyticsLogsPortStub:
    def __init__(self) -> None:
        self.click_query = None
        self.event_query = None
        self.click_log = AnalyticsClickLog(
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
        self.event_log = AnalyticsEventLog(
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

    def list_clicks(self, query):
        self.click_query = query
        return [self.click_log]

    def list_events(self, query):
        self.event_query = query
        return [self.event_log]


class _AuthorizationStub:
    def __init__(self) -> None:
        self.permission_codes: list[str] = []

    def required_user_permission(self, *, permission_code: str, **_: object) -> None:
        self.permission_codes.append(permission_code)


def test_adapter_translates_crm_click_requests_and_analytics_log_values() -> None:
    analytics_port = _AnalyticsLogsPortStub()
    adapter = CrmIngestionAnalyticsLogsAdapter(analytics_port)  # type: ignore[arg-type]

    response = adapter.list_clicks(
        ListClickLogsCommand(
            crm_user_id=7,
            app_id=11,
            click_id="click-1",
            start_at=datetime(2026, 7, 30, 12, tzinfo=timezone(timedelta(hours=3))),
            end_at=datetime(2026, 7, 30, 15, tzinfo=timezone(timedelta(hours=3))),
            limit=25,
            offset=50,
        )
    )

    assert analytics_port.click_query.app_id == 11
    assert analytics_port.click_query.click_id == "click-1"
    assert analytics_port.click_query.pagination.start_at == datetime(2026, 7, 30, 9, tzinfo=UTC)
    assert analytics_port.click_query.pagination.end_at == datetime(2026, 7, 30, 12, tzinfo=UTC)
    assert analytics_port.click_query.pagination.limit == 25
    assert analytics_port.click_query.pagination.offset == 50
    assert response.clicks[0].click_id == "click-1"
    assert response.clicks[0].normalized_params == {"campaign": "spring"}

    response.clicks[0].raw_query["campaign"] = "changed"
    response.clicks[0].normalized_params["campaign"] = "changed"

    assert analytics_port.click_log.raw_query == {"campaign": "spring"}
    assert analytics_port.click_log.normalized_params == {"campaign": "spring"}


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

    response.events[0].payload["order_id"] = "changed"

    assert analytics_port.event_log.payload == {"order_id": "order-1"}


def test_ingestion_data_service_reads_analytics_logs_through_the_adapter() -> None:
    analytics_port = _AnalyticsLogsPortStub()
    authorization = _AuthorizationStub()
    service = IngestionDataService(
        analytics_logs_gateway=CrmIngestionAnalyticsLogsAdapter(analytics_port),  # type: ignore[arg-type]
        uow_factory=StubUoWFactory(StubUnitOfWork()),
        authorization_service=authorization,  # type: ignore[arg-type]
    )

    response = service.list_clicks(ListClickLogsCommand(crm_user_id=7, app_id=11, click_id="click-1"))

    assert [click.click_id for click in response.clicks] == ["click-1"]
    assert authorization.permission_codes == [CrmPermissionEntity.view_raw_logs_permission()]
