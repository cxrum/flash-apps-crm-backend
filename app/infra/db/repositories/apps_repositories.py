from __future__ import annotations

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.domain.app.CrmAppEntity import CrmAppEntity
from app.domain.app.app_repository_protocol import CrmAppRepositoryProtocol
from app.domain.app_platform.CrmAppPlatformEntity import CrmAppPlatformEntity
from app.domain.app_platform.app_platform_repository_protocol import CrmAppPlatformRepositoryProtocol
from app.domain.app_user.CrmAppUserEntity import CrmAppUserEntity
from app.domain.app_user.app_user_repository_protocol import CrmAppUserRepositoryProtocol
from app.domain.install.CrmInstallEntity import CrmInstallEntity
from app.domain.install.install_repository_protocol import CrmInstallRepositoryProtocol
from app.infra.db.apps.models import App, AppPlatform, AppUser, Install


class SqlAlchemyCrmAppRepository(CrmAppRepositoryProtocol):
    def __init__(self, session: Session) -> None:
        self.session = session

    def _to_domain(self, row: App) -> CrmAppEntity:
        return CrmAppEntity(
            app_id=row.app_id,
            name=row.name,
            code_slug=row.code_slug,
            description=row.description,
            tech_description=row.tech_description,
            status=row.status,
            logo_url=row.logo_url,
            screenshots=list(row.screenshots),
            created_at=row.created_at,
            updated_at=row.updated_at,
        )

    def _to_row(self, entity: CrmAppEntity) -> App:
        kwargs: dict[str, object] = {
            "name": entity.name,
            "code_slug": entity.code_slug,
            "description": entity.description,
            "tech_description": entity.tech_description,
            "status": entity.status,
            "logo_url": entity.logo_url,
            "screenshots": list(entity.screenshots),
        }
        if entity.app_id is not None:
            kwargs["app_id"] = entity.app_id
        if entity.created_at is not None:
            kwargs["created_at"] = entity.created_at
        if entity.updated_at is not None:
            kwargs["updated_at"] = entity.updated_at
        return App(**kwargs)

    def save(self, entity: CrmAppEntity) -> CrmAppEntity:
        row = self.session.merge(self._to_row(entity))
        self.session.flush()
        return self._to_domain(row)

    def save_many(self, entities: list[CrmAppEntity]) -> list[CrmAppEntity]:
        rows = [self.session.merge(self._to_row(entity)) for entity in entities]
        self.session.flush()
        return [self._to_domain(row) for row in rows]

    def get_by_id(self, app_id: int) -> CrmAppEntity | None:
        row = self.session.get(App, app_id)
        return self._to_domain(row) if row is not None else None

    def get_by_slug(self, code_slug: str) -> CrmAppEntity | None:
        row = self.session.scalars(
            select(App).where(App.code_slug == code_slug)
        ).first()
        return self._to_domain(row) if row is not None else None

    def list_all(self) -> list[CrmAppEntity]:
        rows = self.session.scalars(select(App).order_by(App.app_id.asc())).all()
        return [self._to_domain(row) for row in rows]


class SqlAlchemyCrmAppPlatformRepository(CrmAppPlatformRepositoryProtocol):
    def __init__(self, session: Session) -> None:
        self.session = session

    def _to_domain(self, row: AppPlatform) -> CrmAppPlatformEntity:
        return CrmAppPlatformEntity(
            platform_id=row.platform_id,
            app_id=row.app_id,
            platform=row.platform,
            package_name=row.package_name,
            store_url=row.store_url,
            install_key=row.install_key,
            sdk_public_key=row.sdk_public_key,
            sdk_secret_hash=row.sdk_secret_hash,
            status=row.status,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )

    def _to_row(self, entity: CrmAppPlatformEntity) -> AppPlatform:
        kwargs: dict[str, object] = {
            "app_id": entity.app_id,
            "platform": entity.platform,
            "package_name": entity.package_name,
            "store_url": entity.store_url,
            "install_key": entity.install_key,
            "sdk_public_key": entity.sdk_public_key,
            "sdk_secret_hash": entity.sdk_secret_hash,
            "status": entity.status,
        }
        if entity.platform_id is not None:
            kwargs["platform_id"] = entity.platform_id
        if entity.created_at is not None:
            kwargs["created_at"] = entity.created_at
        if entity.updated_at is not None:
            kwargs["updated_at"] = entity.updated_at
        return AppPlatform(**kwargs)

    def save(self, entity: CrmAppPlatformEntity) -> CrmAppPlatformEntity:
        row = self.session.merge(self._to_row(entity))
        self.session.flush()
        return self._to_domain(row)

    def save_many(self, entities: list[CrmAppPlatformEntity]) -> list[CrmAppPlatformEntity]:
        rows = [self.session.merge(self._to_row(entity)) for entity in entities]
        self.session.flush()
        return [self._to_domain(row) for row in rows]

    def get_by_id(self, platform_id: int) -> CrmAppPlatformEntity | None:
        row = self.session.get(AppPlatform, platform_id)
        return self._to_domain(row) if row is not None else None

    def get_by_install_key(self, install_key: str) -> CrmAppPlatformEntity | None:
        row = self.session.scalars(
            select(AppPlatform)
            .where(AppPlatform.install_key == install_key)
            .order_by(AppPlatform.platform_id.asc())
        ).first()
        return self._to_domain(row) if row is not None else None
    
    def list_by_app_id(self, app_id: int) -> list[CrmAppPlatformEntity]:
        rows = self.session.scalars(
            select(AppPlatform)
            .where(AppPlatform.app_id == app_id)
            .order_by(AppPlatform.platform_id.asc())
        ).all()
        return [self._to_domain(row) for row in rows]

    def list_by_platform(self, platform: str) -> list[CrmAppPlatformEntity]:
        rows = self.session.scalars(
            select(AppPlatform)
            .where(AppPlatform.platform == platform)
            .order_by(AppPlatform.platform_id.asc())
        ).all()
        return [self._to_domain(row) for row in rows]


class SqlAlchemyCrmAppUserRepository(CrmAppUserRepositoryProtocol):
    def __init__(self, session: Session) -> None:
        self.session = session

    def _to_domain(self, row: AppUser) -> CrmAppUserEntity:
        return CrmAppUserEntity(
            app_id=row.app_id,
            app_user_id=row.app_user_id,
            created_at=row.created_at,
        )

    def _to_row(self, entity: CrmAppUserEntity) -> AppUser:
        kwargs: dict[str, object] = {
            "app_id": entity.app_id,
        }
        if entity.app_user_id is not None:
            kwargs["app_user_id"] = entity.app_user_id
        if entity.created_at is not None:
            kwargs["created_at"] = entity.created_at
        return AppUser(**kwargs)

    def save(self, entity: CrmAppUserEntity) -> CrmAppUserEntity:
        row = self.session.merge(self._to_row(entity))
        self.session.flush()
        return self._to_domain(row)

    def save_many(self, entities: list[CrmAppUserEntity]) -> list[CrmAppUserEntity]:
        rows = [self.session.merge(self._to_row(entity)) for entity in entities]
        self.session.flush()
        return [self._to_domain(row) for row in rows]

    def get_by_id(self, app_user_id: int) -> CrmAppUserEntity | None:
        row = self.session.get(AppUser, app_user_id)
        return self._to_domain(row) if row is not None else None

    def list_by_app_id(self, app_id: int) -> list[CrmAppUserEntity]:
        rows = self.session.scalars(
            select(AppUser)
            .where(AppUser.app_id == app_id)
            .order_by(AppUser.app_user_id.asc())
        ).all()
        return [self._to_domain(row) for row in rows]


class SqlAlchemyCrmInstallRepository(CrmInstallRepositoryProtocol):
    def __init__(self, session: Session) -> None:
        self.session = session

    def _to_domain(self, row: Install) -> CrmInstallEntity:
        return CrmInstallEntity(
            install_id=row.install_id,
            click_id=row.click_id,
            app_user_id=row.app_user_id,
            app_platform_id=row.app_platform_id,
            device_data=dict(row.device_data),
            installed_at=row.installed_at,
        )

    def _to_row(self, entity: CrmInstallEntity) -> Install:
        kwargs: dict[str, object] = {
            "click_id": entity.click_id,
            "app_user_id": entity.app_user_id,
            "app_platform_id": entity.app_platform_id,
            "device_data": dict(entity.device_data),
        }
        if entity.install_id is not None:
            kwargs["install_id"] = entity.install_id
        if entity.installed_at is not None:
            kwargs["installed_at"] = entity.installed_at
        return Install(**kwargs)

    def save(self, entity: CrmInstallEntity) -> CrmInstallEntity:
        row = self.session.merge(self._to_row(entity))
        self.session.flush()
        return self._to_domain(row)

    def save_many(self, entities: list[CrmInstallEntity]) -> list[CrmInstallEntity]:
        rows = [self.session.merge(self._to_row(entity)) for entity in entities]
        self.session.flush()
        return [self._to_domain(row) for row in rows]

    def get_by_id(self, install_id: int) -> CrmInstallEntity | None:
        row = self.session.get(Install, install_id)
        return self._to_domain(row) if row is not None else None

    def get_by_app_user_id(self, app_user_id: int) -> CrmInstallEntity | None:
        row = self.session.scalars(
            select(Install)
            .where(Install.app_user_id == app_user_id)
            .order_by(desc(Install.installed_at), desc(Install.install_id))
        ).first()
        return self._to_domain(row) if row is not None else None
    
    def get_by_click_id(self, click_id: str) -> CrmInstallEntity | None:
        row = self.session.scalars(
            select(Install)
            .where(Install.click_id == click_id)
            .order_by(desc(Install.installed_at), desc(Install.install_id))
        ).first()
        return self._to_domain(row) if row is not None else None
