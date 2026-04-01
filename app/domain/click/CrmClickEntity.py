from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
import uuid

from app.domain.exceptions import DomainError
from app.domain.param_definition.CrmParamDefinitionEntity import CrmParamDefinitionEntity


@dataclass()
class CrmClickEntity:
    click_id: str
    app_platform_id: int
    status: str = "accepted"
    raw_query: dict[str, Any] = field(default_factory=dict)
    ip_address: str | None = None
    user_agent: str | None = None
    country_code: str | None = None
    region: str | None = None
    city: str | None = None
    language: str | None = None
    referrer: str | None = None
    source: str | None = None
    redirect_target: str | None = None
    normalized_params: dict[str, Any] = field(default_factory=dict)
    created_at: datetime | None = None
    
    @classmethod
    def create_synthetic(
        cls,
        app_platform_id: int,
        params: dict,
    ) -> "CrmClickEntity":
        return cls(
            click_id = CrmClickEntity.generate_click_id(),
            app_platform_id=app_platform_id,
            raw_query=params,
            source="sdk_install",
        )
    
    def normalize_params(self, defenitions: list[CrmParamDefinitionEntity]) -> None:
        self.normalized_params = {}
        
        for definition in defenitions:
            value = definition.get_param_value(self.raw_query)
            self.normalized_params[definition.machine_key] = value
        

    @staticmethod
    def generate_click_id() -> str:
        return str(uuid.uuid4())
    
    def set_new_click_id(self):
        self.click_id = str(uuid.uuid4())
    
    def accepted(self) -> None:
        self.status = 'accepted'
        
    def rejected(self) -> None:
        self.status = 'rejected'
        
    def duplicate(self) -> None:
        self.status = 'duplicate' 
        
    def redirected(self) -> None:
        self.status = 'redirected' 
    
    def validate_click_status(self) -> None:
        if self.status not in ['accepted', 'redirected', 'duplicate', 'rejected', 'test']:
            raise DomainError(f"Click has incorrect status")
    
    def validate_platform_match(self, expected_platform_id: int) -> None:
        if self.app_platform_id != expected_platform_id:
            raise DomainError(f"Click {self.click_id} belongs to another platform")