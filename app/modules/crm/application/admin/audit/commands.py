from app.modules.crm.application.base import PaginationCommand


class ListAuditLogCommand(PaginationCommand):
    crm_user_id: int
    app_id: int | None = None
    actor_id: int | None = None
    entity_type: str | None = None
    entity_id: int | None = None
