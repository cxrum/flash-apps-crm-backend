from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal

@dataclass
class CrmAppSecretEntity:
    template_id: int
    encrypted_value: str
    platform_id: int | None = None
    active_flag: bool = True
    version: float = 1
    secret_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def update(
        self,
        *,
        template_id: int | None = None,
        encrypted_value: str | None = None,
        platform_id: int | None = None,
        active_flag: bool | None = None,
        version: float | None = None,
    ) -> None:
        self.template_id = template_id if template_id is not None else self.template_id
        self.encrypted_value = encrypted_value if encrypted_value is not None else self.encrypted_value
        self.platform_id = platform_id if platform_id is not None else self.platform_id
        self.active_flag = active_flag if active_flag is not None else self.active_flag
        self.version = version if version is not None else self.version

        self.updated_at = datetime.now(UTC)
