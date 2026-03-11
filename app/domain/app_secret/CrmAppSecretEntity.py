from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True)
class CrmAppSecretEntity:
    template_id: int
    encrypted_value: str
    platform_id: int | None = None
    active_flag: bool = True
    version: Decimal = Decimal("1")
    secret_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
