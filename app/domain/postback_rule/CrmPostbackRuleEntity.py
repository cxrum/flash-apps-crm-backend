from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class CrmPostbackRuleEntity:
    platfrom_app_id: int
    name: str
    endpoint_url: str
    trigger_type: str
    http_method: str = "POST"
    headers: dict[str, Any] = field(default_factory=dict)
    auth_params: dict[str, Any] = field(default_factory=dict)
    timeout: int = 0
    event_key: str | None = None
    template: dict[str, Any] = field(default_factory=dict)
    retry_policy: dict[str, Any] = field(default_factory=dict)
    is_active: bool = True
    rule_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
