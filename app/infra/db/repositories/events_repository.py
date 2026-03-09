from __future__ import annotations

from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import Session

from app.domain.events.entities import EventEntity
from app.infra.db.models import Event
from app.domain.events.events_repository_protocol import EventsRepositoryProtocol


class EventsRepository(EventsRepositoryProtocol):
    def __init__(self, db: Session) -> None:
        self.db = db
        
    def insert_events(self, events: list[EventEntity]) -> int:
        if not events:
            return 0
        rows = [
            {
                "event_id": event.event_id,
                "app_id": event.app_id,
                "event_name": event.event_name,
                "event_time": event.event_time,
                "platform": event.platform,
                "anonymous_id": event.anonymous_id,
                "user_id": event.user_id,
                "source": event.source,
                "campaign": event.campaign,
                "medium": event.medium,
                "params": event.params,
            }
            for event in events
        ]
        stmt = pg_insert(Event).values(rows)
        result = self.db.execute(stmt.on_conflict_do_nothing(index_elements=[Event.event_id]))
        return result.rowcount if result.rowcount is not None and result.rowcount > 0 else 0
