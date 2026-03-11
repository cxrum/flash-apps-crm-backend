from __future__ import annotations

from dataclasses import dataclass

from app.domain.app.app_repository_protocol import CrmAppRepositoryProtocol
from app.domain.app_user.app_user_repository_protocol import CrmAppUserRepositoryProtocol
from app.domain.events.CrmEventEntity import EventEntity
from app.domain.events.event_repository_protocol import CrmEventRepositoryProtocol
from app.domain.user.CrmUserEntity import CrmUserEntity
from app.domain.user.user_repository_protocol import CrmUserRepositoryProtocol

class DomainAppNotFoundError(Exception):
    pass

@dataclass
class BatchIngestResult:
    status: str
    received: int
    inserted: int
    ignored_duplicates: int

    def as_dict(self) -> dict[str, int | str]:
        return {
            "status": self.status,
            "received": self.received,
            "inserted": self.inserted,
            "ignored_duplicates": self.ignored_duplicates,
        }


class EventsDomainService:
    def __init__(
        self, 
        event_repo: CrmEventRepositoryProtocol,
        app_repo: CrmAppRepositoryProtocol,
        ) -> None:
        
        self.event_repo = event_repo
        self.app_repo = app_repo

    def process_batch(self, *, app_id: int, events: list[EventEntity], received: int) -> BatchIngestResult:
        if not self.app_repo.get_by_id(app_id):
            raise DomainAppNotFoundError("Unknown app id")

        inserted_events = self.event_repo.insert_many(events)
        inserted = len(inserted_events)

        return BatchIngestResult(
            status="accepted",
            received=received,
            inserted=inserted,
            ignored_duplicates=received - inserted,
        )
