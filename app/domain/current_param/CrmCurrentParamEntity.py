from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Any


@dataclass(frozen=True)
class CrmCurrentParamEntity:
    click_id: str
    param_key: str
    value_string: str | None = None
    value_number: Decimal | None = None
    value_bool: bool | None = None
    value_json: dict[str, Any] | list[Any] | None = None
    updated_at: datetime | None = None
