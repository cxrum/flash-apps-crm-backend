from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CrmMetricDefinitionEntity:
    machine_key: str
    display_name: str
    app_id: int | None = None
    description: str | None = None
    enabled: bool = True
    visible_in_stats: bool = True
    visible_in_logs: bool = True
    metric_definition_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
