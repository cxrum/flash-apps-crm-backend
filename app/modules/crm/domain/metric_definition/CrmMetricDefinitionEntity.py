from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass
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

    def update(self, *, 
        machine_key: str | None = None,
        display_name: str | None = None,
        description: str | None = None,
        enabled: bool | None = None,
        visible_in_stats: bool = True,
        visible_in_logs: bool = True,
    ) -> None:
        
        self.machine_key = machine_key if machine_key is not None else self.machine_key
        self.display_name = display_name if display_name is not None else self.display_name
        self.description = description if description is not None else self.description
        self.enabled = enabled if enabled is not None else self.enabled
        self.visible_in_stats = visible_in_stats if visible_in_stats is not None else self.visible_in_stats
        self.visible_in_logs = visible_in_logs if visible_in_logs is not None else self.visible_in_logs
        
        self.updated_at = datetime.now(UTC)
        