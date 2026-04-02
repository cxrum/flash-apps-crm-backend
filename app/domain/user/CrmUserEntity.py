from dataclasses import dataclass
from datetime import UTC, datetime

from app.domain.hash_protocol import HashableValue


@dataclass
class CrmUserEntity:
    full_name: str
    email: str
    password_hash: HashableValue
    time_zone: str
    is_active: bool = True
    user_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def update(
        self,
        *,
        full_name: str | None = None,
        email: str | None = None,
        password_hash: HashableValue | None = None,
        is_active: bool | None = None,
    ) -> None:
        self.full_name = full_name if full_name is not None else self.full_name
        self.email = email if email is not None else self.email
        self.password_hash = password_hash if password_hash is not None else self.password_hash
        self.is_active = is_active if is_active is not None else self.is_active

        self.updated_at = datetime.now(UTC)

    