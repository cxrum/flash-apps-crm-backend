from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass
class CrmUserAppAccessEntity:
    user_id: int
    app_id: int
    role_id: int
    assigned_at: datetime | None = None

    def update(
        self,
        *,
        user_id: int | None = None,
        app_id: int | None = None,
        role_id: int | None = None,
        assigned_at: datetime | None = None,
    ) -> None:
        self.user_id = user_id if user_id is not None else self.user_id
        self.app_id = app_id if app_id is not None else self.app_id
        self.role_id = role_id if role_id is not None else self.role_id
        self.assigned_at = assigned_at if assigned_at is not None else datetime.now(UTC)
