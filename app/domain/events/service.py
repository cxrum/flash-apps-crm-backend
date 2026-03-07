from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.domain.events.entities import EventEntity
from app.domain.events.mappers import EventEntityMapper, EventPersistenceMapper
from app.infra.db.repositories.app_repository_protocol import AppRepositoryProtocol
from app.infra.db.repositories.events_repository_protocol import EventsRepositoryProtocol
from app.infra.db.repositories.identity_repository_protocol import IdentityRepositoryProtocol
from app.infra.db.repositories.user_repository_protocol import UserRepositoryProtocol

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
        indentity_repo: IdentityRepositoryProtocol
        ) -> None:
        
        self.event_repo = event_repo
        self.app_repo = app_repo
        self.user_repo = user_repo
        self.indentity_repo = indentity_repo

    def process_batch(self, *, app_id: int, environment: str, batch_payload: dict) -> BatchIngestResult:
        if not self.app_repo.exists(app_id):
            raise DomainAppNotFoundError("Unknown app id")

        events_data: list[dict] = batch_payload["events"]
        received = len(events_data)
        sdk_version: str = batch_payload["sdk_version"]
        sent_at: datetime = batch_payload["sent_at"]

        events = [
            EventEntityMapper.from_dict(
                event_data,
                app_id=app_id,
                environment=environment,
                sdk_version=sdk_version,
                sent_at=sent_at,
            )
            for event_data in events_data
        ]
        event_dtos = [EventPersistenceMapper.to_dto(event) for event in events]

        user_ids = sorted({event.user_id for event in events if event.user_id})
        identity_links = self._collect_identity_links(events)

        try:
            self.user_repo.upsert_users(user_ids)
            self.indentity_repo.upsert_identities(identity_links)
            inserted = self.event_repo.insert_events(event_dtos)
            
            self.event_repo.commit()
            self.indentity_repo.commit()
            self.event_repo.commit()
            
        except Exception:
            self.event_repo.rollback()
            self.indentity_repo.rollback()
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
