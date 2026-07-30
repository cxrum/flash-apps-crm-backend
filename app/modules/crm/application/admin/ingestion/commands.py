from app.modules.crm.application.base import PaginationCommand


class ListClickLogsCommand(PaginationCommand):
    crm_user_id: int
    app_id: int
    click_id: str | None = None


class ListEventLogsCommand(PaginationCommand):
    crm_user_id: int
    app_id: int
    click_id: str | None = None
    event_key: str | None = None
