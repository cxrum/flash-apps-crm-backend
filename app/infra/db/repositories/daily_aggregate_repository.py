from __future__ import annotations

from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import Session

from app.infra.db.models import DailyAggregate
from app.domain.contracts.daily_aggregate_repository_protocol import DailyAggregateRepositoryProtocol


class DailyAggregateRepository(DailyAggregateRepositoryProtocol):
    def __init__(self, db: Session) -> None:
        self.db = db

    def upsert_daily_aggregate(self, aggregate: dict) -> None:
        stmt = pg_insert(DailyAggregate).values([aggregate])
        self.db.execute(
            stmt.on_conflict_do_update(
                index_elements=[
                    DailyAggregate.app_id,
                    DailyAggregate.date,
                    DailyAggregate.platform,
                ],
                set_={
                    "installs": stmt.excluded.installs,
                    "signups": stmt.excluded.signups,
                    "revenue": stmt.excluded.revenue,
                    "active_subs": stmt.excluded.active_subs,
                },
            )
        )

    def commit(self) -> None:
        self.db.commit()

    def rollback(self) -> None:
        self.db.rollback()
