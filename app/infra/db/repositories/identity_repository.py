from __future__ import annotations

from datetime import datetime

from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import Session

from app.infra.db.models import Identity, User
from app.infra.db.repositories.identity_repository_protocol import IdentityRepositoryProtocol


class IdentityRepository(IdentityRepositoryProtocol):
    def __init__(self, db: Session) -> None:
        self.db = db

    def upsert_user(self, user_id: str) -> None:
        stmt = pg_insert(User).values([{"user_id": user_id}])
        self.db.execute(stmt.on_conflict_do_nothing(index_elements=[User.user_id]))

    def upsert_identity(self, *, anonymous_id: str, user_id: str, linked_at: datetime) -> None:
        stmt = pg_insert(Identity).values(
            [
                {
                    "anonymous_id": anonymous_id,
                    "user_id": user_id,
                    "first_seen_at": linked_at,
                }
            ]
        )
        self.db.execute(
            stmt.on_conflict_do_update(
                index_elements=[Identity.anonymous_id],
                set_={"user_id": stmt.excluded.user_id},
                where=stmt.excluded.user_id.is_not(None),
            )
        )
        
    def upsert_identities(self, identity_links: dict[str, str | None]) -> None:
        identity_rows = [
            {
                "anonymous_id": anon_id, 
                "user_id": user_id
             } for anon_id, user_id in identity_links.items()
            ]
        
        if not identity_rows:
            return
        
        stmt = pg_insert(Identity).values(identity_rows)
        
        self.db.execute(
                stmt.on_conflict_do_update(
                index_elements=[Identity.anonymous_id],
                set_={"user_id": stmt.excluded.user_id},
                where=stmt.excluded.user_id.is_not(None),
            )
        )
        
        
    def commit(self) -> None:
        self.db.commit()

    def rollback(self) -> None:
        self.db.rollback()
