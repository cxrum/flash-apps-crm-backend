from app.modules.crm.application.admin.ingestion.commands import ListClickLogsCommand
from app.modules.crm.application.admin.ingestion.responses import ClickLogResponseEntry, ListClickLogsResponse
from app.modules.crm.application.admin.ingestion.service import IngestionDataService
from app.modules.crm.domain.permission.CrmPermissionEntity import CrmPermissionEntity
from tests.unit.doubles.domain.uow import StubUnitOfWork, StubUoWFactory


class _AnalyticsLogsGatewayStub:
    def __init__(self) -> None:
        self.command: ListClickLogsCommand | None = None

    def list_clicks(self, command: ListClickLogsCommand) -> ListClickLogsResponse:
        self.command = command
        return ListClickLogsResponse(clicks=[ClickLogResponseEntry(click_id="click-1", app_platform_id=1)])

    def list_raw_events(self, command):
        raise AssertionError(f"Unexpected event request: {command}")


class _AuthorizationStub:
    def __init__(self) -> None:
        self.permission_codes: list[str] = []

    def required_user_permission(self, *, permission_code: str, **_: object) -> None:
        self.permission_codes.append(permission_code)


def test_ingestion_data_service_authorizes_then_delegates_to_its_analytics_gateway() -> None:
    gateway = _AnalyticsLogsGatewayStub()
    authorization = _AuthorizationStub()
    service = IngestionDataService(
        analytics_logs_gateway=gateway,  # type: ignore[arg-type]
        uow_factory=StubUoWFactory(StubUnitOfWork()),
        authorization_service=authorization,  # type: ignore[arg-type]
    )
    command = ListClickLogsCommand(crm_user_id=3, app_id=9)

    response = service.list_clicks(command)

    assert gateway.command == command
    assert authorization.permission_codes == [CrmPermissionEntity.view_raw_logs_permission()]
    assert [click.click_id for click in response.clicks] == ["click-1"]
