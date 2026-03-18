from datetime import datetime
from typing import Any

from app.domain.event_bus.entity import DomainEventMessage
from app.domain.exceptions import DomainError


class UpdateCurrentParamMessage(DomainEventMessage):
    EVENT_NAME = "sdk.update.current_params.request"
    
    @property
    def click_id(self) -> str:
        return str(self.payload["click_id"])
    
    @property
    def params(self) -> dict:
        return dict(self.payload["params"])
    
    @property
    def updated_at(self) -> datetime:
        value = self.payload["updated_at"]
        if not isinstance(value, datetime):
            raise DomainError("UpdateCurrentParamMessage.updated_at must be datetime")
        return value