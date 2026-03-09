from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.app.entities import AppEntity
from app.infra.db.models import App
from app.domain.app.app_repository_protocol import AppRepositoryProtocol


class AppRepository(AppRepositoryProtocol):
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, app_id: int) -> AppEntity | None:
        
        app = self.db.execute(select(App).where(App.app_id == app_id)).scalar_one_or_none()
        
        if app is None:
            return None
        
        return AppEntity(
            app_id=app.app_id,
            app_secret_hash=app.app_secret_hash,
            created_at=app.created_at
        )

    def exists(self, app_id: int) -> bool:
        return self.get_by_id(app_id) is not None

    def create(self, app_secret_hash: str) -> AppEntity:
        app = App(app_secret_hash=app_secret_hash)
        self.db.add(app)
        self.db.flush()
        
        return AppEntity(
            app_id=app.app_id,
            app_secret_hash=app.app_secret_hash,
            created_at=app.created_at
        )
