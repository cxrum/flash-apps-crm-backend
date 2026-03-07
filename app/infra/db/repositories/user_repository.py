from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import Session

from app.infra.db.models import User
from app.infra.db.repositories.user_repository_protocol import UserRepositoryProtocol


class UserRepository(UserRepositoryProtocol):
    def __init__(self, db: Session) -> None:
        self.db = db

    def upsert_user(self, *, user_id: str, created_at: datetime | None = None) -> None:
        stmt = pg_insert(User).values(
            [
                {
                    "user_id": user_id,
                    "created_at": created_at
                }
            ]
        )
        
        self.db.execute(
            stmt.on_conflict_do_nothing(
                index_elements=[User.user_id]
            )
        )

    def upsert_users(self, user_ids: list[str], *, created_at: datetime | None = None) -> None:
        if not user_ids:
            return

        resolved_created_at = created_at or None
        rows = [
            {
                "user_id": user_id,
                "created_at": resolved_created_at,
            }
            for user_id in sorted(set(user_ids))
        ]
        stmt = pg_insert(User).values(rows)
        self.db.execute(stmt.on_conflict_do_nothing(index_elements=[User.user_id]))


    def commit(self) -> None:
        self.db.commit()

    def rollback(self) -> None:
        self.db.rollback()
