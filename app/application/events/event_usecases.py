

from datetime import datetime
from hashlib import sha256
import hmac

from app.application.events.entities import IngestEventsBatchCommand
from app.application.events.entities import EventItemCommand
from app.core.config import Settings
from app.domain.events.mappers import EventEntityMapper
from app.domain.events.service import EventsDomainService

class InvalidSignatureException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class EventUseCases:
    def __init__(
        self, 
        event_domain_service: EventsDomainService
        ) -> None:
        self.event_domain_service = event_domain_service
    
    def process_batch(self, command: IngestEventsBatchCommand):
        events_data: list[EventItemCommand] = command.payload.events
        received = len(events_data)
        sdk_version: str = command.payload.sdk_version
        sent_at: datetime = command.payload.sent_at

        events = [
            EventEntityMapper.from_payload(
                event_data,
                app_id=command.app_id,
                environment=command.env,
                sdk_version=sdk_version,
                sent_at=sent_at,
            )
            for event_data in events_data
        ]
        result = self.event_domain_service.process_batch(
                app_id=command.app_id,
                events=events,
                received=received
            )
        
        return result
