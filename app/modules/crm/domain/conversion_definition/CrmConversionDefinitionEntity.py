from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass
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
    
    def update(self, *, 
        machine_key: str | None = None,
        display_name: str | None = None,
        description: str | None = None,
        revenue_enabled: bool | None = None,
        expects_amount: bool | None = None,
        expects_currency: bool | None = None,
        dedup_mode: str | None = None ,
    ) -> None:
        
        self.machine_key = machine_key if machine_key is not None else self.machine_key
        self.display_name = display_name if display_name is not None else self.display_name
        self.description = description if description is not None else self.description
        self.revenue_enabled = revenue_enabled if revenue_enabled is not None else self.revenue_enabled
        self.expects_amount = expects_amount if expects_amount is not None else self.expects_amount
        self.expects_currency = expects_currency if expects_currency is not None else self.expects_currency
        self.dedup_mode = dedup_mode if dedup_mode is not None and dedup_mode in self._dedup_modes() else self.dedup_mode
        
        self.updated_at = datetime.now(UTC)
        
    @staticmethod
    def _dedup_modes() -> list[str]:
        return ["none"]