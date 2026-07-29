from types import TracebackType

from app.modules.analytics.application.admin.logs.service import AnalyticsLogsService
from app.modules.analytics.domain.click.AnalyticsClickEntity import AnalyticsClickEntity
from app.modules.crm.application.admin.logs.commands import ListClickLogsCommand
from app.modules.crm.domain.pagination import Pagination


class _ClickRepository:
    def __init__(self, clicks: list[AnalyticsClickEntity]) -> None:
        self._clicks = clicks

    def list_by_app_id(
        self,
        app_id: int,
        *,
        click_id: str | None = None,
        pagination: Pagination | None = None,
    ) -> list[AnalyticsClickEntity]:
        assert app_id == 1
        return [click for click in self._clicks if click_id is None or click.click_id == click_id]


class _AnalyticsLogsUnitOfWork:
    def __init__(self, clicks: list[AnalyticsClickEntity]) -> None:
        self.click_repo = _ClickRepository(clicks)

    def __enter__(self) -> "_AnalyticsLogsUnitOfWork":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        return None


class _AnalyticsLogsUnitOfWorkFactory:
    def __init__(self, uow: _AnalyticsLogsUnitOfWork) -> None:
        self._uow = uow

    def create(self) -> _AnalyticsLogsUnitOfWork:
        return self._uow


def test_analytics_logs_service_reads_clicks_without_crm_authorization() -> None:
    click = AnalyticsClickEntity(click_id="analytics-click", app_platform_id=1)
    service = AnalyticsLogsService(_AnalyticsLogsUnitOfWorkFactory(_AnalyticsLogsUnitOfWork([click])))  # type: ignore[arg-type]

    response = service.list_clicks(ListClickLogsCommand(crm_user_id=1, app_id=1))

    assert [item.click_id for item in response.clicks] == [click.click_id]
