from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.infra.db.models import App
from app.domain.app.app_repository_protocol import AppRepositoryProtocol


class AppRepository(AppRepositoryProtocol):
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, app_id: int) -> App | None:
        return self.db.execute(select(App).where(App.app_id == app_id)).scalar_one_or_none()

    def exists(self, app_id: int) -> bool:
        return self.get_by_id(app_id) is not None

    def create(self, app_secret_hash: str) -> App:
        app = App(app_secret_hash=app_secret_hash)
        self.db.add(app)
        self.db.flush()
        return app

    def commit(self) -> None:
        self.db.commit()

    def rollback(self) -> None:
        self.db.rollback()

