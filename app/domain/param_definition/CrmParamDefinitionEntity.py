from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CrmParamDefinitionEntity:
    display_name: str
    machine_key: str
    data_type: str
    app_id: int | None = None
    description: str | None = None
    overwrite_policy: str = "replace"
    is_active: bool = True
    visible_in_logs: bool = True
    visible_in_stats: bool = False
    filterable: bool = False
    groupable: bool = False
    param_definition_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
