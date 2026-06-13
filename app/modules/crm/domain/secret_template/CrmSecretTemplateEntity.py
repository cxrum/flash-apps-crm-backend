from dataclasses import dataclass
from datetime import UTC, datetime

@dataclass
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

    def is_client_public(self) -> bool:
        return self.scope == "client_public"
    
    def is_server_private(self) -> bool:
        return self.scope == "server_private"
    
    @staticmethod
    def mask(value: str) -> str:
        _new_value = "***"
        
        if len(value) > 3:
            _new_value = value[:3] + _new_value
        
        return _new_value

    def update(
        self,
        *,
        code: str | None = None,
        display_name: str | None = None,
        scope: str | None = None,
        value_type: str | None = None,
        is_masked: bool | None = None,
        is_required: bool | None = None,
    ) -> None:
        self.code = code if code is not None else self.code
        self.display_name = display_name if display_name is not None else self.display_name
        self.scope = scope if scope is not None else self.scope
        self.value_type = value_type if value_type is not None else self.value_type
        self.is_masked = is_masked if is_masked is not None else self.is_masked
        self.is_required = is_required if is_required is not None else self.is_required

        self.updated_at = datetime.now(UTC)
