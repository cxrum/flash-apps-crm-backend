from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.domain.events.entities import EventEntity
from app.domain.events.mappers import EventEntityMapper
from app.domain.app.app_repository_protocol import AppRepositoryProtocol
from app.domain.events.events_repository_protocol import EventsRepositoryProtocol
from app.domain.identity.identity_repository_protocol import IdentityRepositoryProtocol
from app.domain.contracts.user_repository_protocol import UserRepositoryProtocol

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
        event_repo: EventsRepositoryProtocol,
        app_repo: AppRepositoryProtocol,
        user_repo: UserRepositoryProtocol,
        identity_repo: IdentityRepositoryProtocol
        ) -> None:
        
        self.event_repo = event_repo
        self.app_repo = app_repo
        self.user_repo = user_repo
        self.identity_repo = identity_repo

    def process_batch(self, *, app_id: int, events: list[EventEntity], received: int) -> BatchIngestResult:
        if not self.app_repo.exists(app_id):
            raise DomainAppNotFoundError("Unknown app id")

        user_ids = sorted({event.user_id for event in events if event.user_id})
        identity_links = self._collect_identity_links(events)

        try:
            self.user_repo.upsert_users(user_ids)
            self.identity_repo.upsert_identities(identity_links)
            inserted = self.event_repo.insert_events(events)

            self.event_repo.commit()
        except Exception:
            self.event_repo.rollback()
            raise

        return BatchIngestResult(
            status="accepted",
            received=received,
            inserted=inserted,
            ignored_duplicates=received - inserted,
        )

    def _collect_identity_links(self, events: list[EventEntity]) -> dict[str, str | None]:
        identity_links: dict[str, str | None] = {}
        for event in events:
            current = identity_links.get(event.anonymous_id)
            identity_links[event.anonymous_id] = current or event.user_id
        return identity_links
