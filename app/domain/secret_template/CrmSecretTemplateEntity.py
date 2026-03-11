from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CrmSecretTemplateEntity:
    code: str
    display_name: str
    scope: str
    value_type: str
    is_masked: bool = True
    is_required: bool = False
    template_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
