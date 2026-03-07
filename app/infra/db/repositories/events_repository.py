from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import Session

from app.contracts.events import EventRecordDTO
from app.infra.db.models import App, Event, Identity, User


class EventsRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def app_exists(self, app_id: int) -> bool:
        app_exists = self.db.execute(select(App.app_id).where(App.app_id == app_id)).scalar_one_or_none()
        return app_exists is not None

    def upsert_users(self, user_ids: list[str]) -> None:
        if not user_ids:
            return
        stmt = pg_insert(User).values([{"user_id": user_id} for user_id in user_ids])
        self.db.execute(stmt.on_conflict_do_nothing(index_elements=[User.user_id]))

    def upsert_identities(self, identity_links: dict[str, str | None]) -> None:
        identity_rows = [{"anonymous_id": anon_id, "user_id": user_id} for anon_id, user_id in identity_links.items()]
        if not identity_rows:
            return
        insert_stmt = pg_insert(Identity).values(identity_rows)
        upsert_stmt = insert_stmt.on_conflict_do_update(
            index_elements=[Identity.anonymous_id],
            set_={"user_id": insert_stmt.excluded.user_id},
            where=insert_stmt.excluded.user_id.is_not(None),
        )
        self.db.execute(upsert_stmt)

    def insert_events(self, events: list[EventRecordDTO]) -> int:
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

    def commit(self) -> None:
        self.db.commit()

    def rollback(self) -> None:
        self.db.rollback()
