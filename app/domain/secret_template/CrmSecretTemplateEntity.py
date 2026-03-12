from dataclasses import dataclass
from datetime import datetime

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
    
    