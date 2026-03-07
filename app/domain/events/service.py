from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from app.contracts.events import EventRecordDTO
from app.domain.events.entities import EventEntity
from app.domain.events.mappers import EventEntityMapper, EventPersistenceMapper


class DomainAppNotFoundError(Exception):
    pass


class EventsRepositoryProtocol(Protocol):
    def app_exists(self, app_id: int) -> bool: ...
    def upsert_users(self, user_ids: list[str]) -> None: ...
    def upsert_identities(self, identity_links: dict[str, str | None]) -> None: ...
    def insert_events(self, events: list[EventRecordDTO]) -> int: ...
    def commit(self) -> None: ...
    def rollback(self) -> None: ...


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
    def __init__(self, repository: EventsRepositoryProtocol) -> None:
        self.repository = repository

    def process_batch(self, *, app_id: int, environment: str, batch_payload: dict) -> BatchIngestResult:
        if not self.repository.app_exists(app_id):
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
            self.repository.upsert_users(user_ids)
            self.repository.upsert_identities(identity_links)
            inserted = self.repository.insert_events(event_dtos)
            self.repository.commit()
        except Exception:
            self.repository.rollback()
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
