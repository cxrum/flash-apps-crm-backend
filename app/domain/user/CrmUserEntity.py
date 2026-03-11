from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CrmUserEntity:
    full_name: str
    email: str
    password_hash: str
    is_active: bool = True
    user_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
