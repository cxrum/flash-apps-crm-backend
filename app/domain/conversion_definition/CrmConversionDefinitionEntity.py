from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CrmConversionDefinitionEntity:
    machine_key: str
    display_name: str
    app_id: int | None = None
    description: str | None = None
    revenue_enabled: bool = False
    expects_amount: bool = False
    expects_currency: bool = False
    dedup_mode: str = "none"
    conversion_definition_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
