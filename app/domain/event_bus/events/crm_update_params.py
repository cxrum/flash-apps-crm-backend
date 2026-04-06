from datetime import datetime

from app.domain.event_bus.entity import DomainEventMessage
from app.domain.event_bus.events.exception import InvalidUpdateCurrentParamUpdatedAt


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
            raise InvalidUpdateCurrentParamUpdatedAt()
        return value
