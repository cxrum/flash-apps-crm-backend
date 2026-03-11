from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.permission.CrmPermissionEntity import CrmPermissionEntity
from app.domain.permission.permission_repository_protocol import CrmPermissionRepositoryProtocol
from app.domain.role.CrmRoleEntity import CrmRoleEntity
from app.domain.role.role_repository_protocol import CrmRoleRepositoryProtocol
from app.domain.role_permission.CrmRolePermissionEntity import CrmRolePermissionEntity
from app.domain.role_permission.role_permission_repository_protocol import (
    CrmRolePermissionRepositoryProtocol,
)
from app.domain.user.CrmUserEntity import CrmUserEntity
from app.domain.user.user_repository_protocol import CrmUserRepositoryProtocol
from app.domain.user_role.CrmUserRoleEntity import CrmUserRoleEntity
from app.domain.user_role.user_role_repository_protocol import CrmUserRoleRepositoryProtocol
from app.infra.db.crm.models import (
    CrmPermission,
    CrmRole,
    CrmRolePermission,
    CrmUser,
    CrmUserRole,
)


class SqlAlchemyCrmUserRepository(CrmUserRepositoryProtocol):
    def __init__(self, session: Session) -> None:
        self.session = session

    def _to_domain(self, row: CrmUser) -> CrmUserEntity:
        return CrmUserEntity(
            user_id=row.user_id,
            full_name=row.full_name,
            email=row.email,
            password_hash=row.password_hash,
            is_active=row.is_active,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )

    def _to_row(self, entity: CrmUserEntity) -> CrmUser:
        kwargs: dict[str, object] = {
            "full_name": entity.full_name,
            "email": entity.email,
            "password_hash": entity.password_hash,
            "is_active": entity.is_active,
        }
        if entity.user_id is not None:
            kwargs["user_id"] = entity.user_id
        if entity.created_at is not None:
            kwargs["created_at"] = entity.created_at
        if entity.updated_at is not None:
            kwargs["updated_at"] = entity.updated_at
        return CrmUser(**kwargs)

    def insert(self, entity: CrmUserEntity) -> CrmUserEntity:
        row = self._to_row(entity)
        self.session.add(row)
        self.session.flush()
        return self._to_domain(row)

    def insert_many(self, entities: list[CrmUserEntity]) -> list[CrmUserEntity]:
        rows = [self._to_row(entity) for entity in entities]
        self.session.add_all(rows)
        self.session.flush()
        return [self._to_domain(row) for row in rows]

    def get_by_id(self, user_id: int) -> CrmUserEntity | None:
        row = self.session.get(CrmUser, user_id)
        return self._to_domain(row) if row is not None else None

    def get_by_email(self, email: str) -> CrmUserEntity | None:
        row = self.session.scalars(
            select(CrmUser).where(CrmUser.email == email)
        ).first()
        return self._to_domain(row) if row is not None else None

    def list_all(self) -> list[CrmUserEntity]:
        rows = self.session.scalars(select(CrmUser).order_by(CrmUser.user_id.asc())).all()
        return [self._to_domain(row) for row in rows]


class SqlAlchemyCrmRoleRepository(CrmRoleRepositoryProtocol):
    def __init__(self, session: Session) -> None:
        self.session = session

    def _to_domain(self, row: CrmRole) -> CrmRoleEntity:
        return CrmRoleEntity(
            role_id=row.role_id,
            code=row.code,
            display_name=row.display_name,
            created_at=row.created_at,
        )

    def _to_row(self, entity: CrmRoleEntity) -> CrmRole:
        kwargs: dict[str, object] = {
            "code": entity.code,
            "display_name": entity.display_name,
        }
        if entity.role_id is not None:
            kwargs["role_id"] = entity.role_id
        if entity.created_at is not None:
            kwargs["created_at"] = entity.created_at
        return CrmRole(**kwargs)

    def save(self, entity: CrmRoleEntity) -> CrmRoleEntity:
        row = self.session.merge(self._to_row(entity))
        self.session.flush()
        return self._to_domain(row)

    def save_many(self, entities: list[CrmRoleEntity]) -> list[CrmRoleEntity]:
        rows = [self.session.merge(self._to_row(entity)) for entity in entities]
        self.session.flush()
        return [self._to_domain(row) for row in rows]

    def get_by_id(self, role_id: int) -> CrmRoleEntity | None:
        row = self.session.get(CrmRole, role_id)
        return self._to_domain(row) if row is not None else None

    def get_by_code(self, code: str) -> CrmRoleEntity | None:
        row = self.session.scalars(select(CrmRole).where(CrmRole.code == code)).first()
        return self._to_domain(row) if row is not None else None

    def list_all(self) -> list[CrmRoleEntity]:
        rows = self.session.scalars(select(CrmRole).order_by(CrmRole.role_id.asc())).all()
        return [self._to_domain(row) for row in rows]


class SqlAlchemyCrmPermissionRepository(CrmPermissionRepositoryProtocol):
    def __init__(self, session: Session) -> None:
        self.session = session

    def _to_domain(self, row: CrmPermission) -> CrmPermissionEntity:
        return CrmPermissionEntity(
            permission_id=row.permission_id,
            code=row.code,
            description=row.description,
            created_at=row.created_at,
        )

    def _to_row(self, entity: CrmPermissionEntity) -> CrmPermission:
        kwargs: dict[str, object] = {
            "code": entity.code,
            "description": entity.description,
        }
        if entity.permission_id is not None:
            kwargs["permission_id"] = entity.permission_id
        if entity.created_at is not None:
            kwargs["created_at"] = entity.created_at
        return CrmPermission(**kwargs)

    def save(self, entity: CrmPermissionEntity) -> CrmPermissionEntity:
        row = self.session.merge(self._to_row(entity))
        self.session.flush()
        return self._to_domain(row)

    def save_many(self, entities: list[CrmPermissionEntity]) -> list[CrmPermissionEntity]:
        rows = [self.session.merge(self._to_row(entity)) for entity in entities]
        self.session.flush()
        return [self._to_domain(row) for row in rows]

    def get_by_id(self, permission_id: int) -> CrmPermissionEntity | None:
        row = self.session.get(CrmPermission, permission_id)
        return self._to_domain(row) if row is not None else None

    def get_by_code(self, code: str) -> CrmPermissionEntity | None:
        row = self.session.scalars(select(CrmPermission).where(CrmPermission.code == code)).first()
        return self._to_domain(row) if row is not None else None

    def list_all(self) -> list[CrmPermissionEntity]:
        rows = self.session.scalars(select(CrmPermission).order_by(CrmPermission.permission_id.asc())).all()
        return [self._to_domain(row) for row in rows]


class SqlAlchemyCrmRolePermissionRepository(CrmRolePermissionRepositoryProtocol):
    def __init__(self, session: Session) -> None:
        self.session = session

    def _to_domain(self, row: CrmRolePermission) -> CrmRolePermissionEntity:
        return CrmRolePermissionEntity(
            role_id=row.role_id,
            permission_id=row.permission_id,
            created_at=row.created_at,
        )

    def _to_row(self, entity: CrmRolePermissionEntity) -> CrmRolePermission:
        kwargs: dict[str, object] = {
            "role_id": entity.role_id,
            "permission_id": entity.permission_id,
        }
        if entity.created_at is not None:
            kwargs["created_at"] = entity.created_at
        return CrmRolePermission(**kwargs)

    def save(self, entity: CrmRolePermissionEntity) -> CrmRolePermissionEntity:
        row = self.session.merge(self._to_row(entity))
        self.session.flush()
        return self._to_domain(row)

    def save_many(self, entities: list[CrmRolePermissionEntity]) -> list[CrmRolePermissionEntity]:
        rows = [self.session.merge(self._to_row(entity)) for entity in entities]
        self.session.flush()
        return [self._to_domain(row) for row in rows]

    def list_by_role_id(self, role_id: int) -> list[CrmRolePermissionEntity]:
        rows = self.session.scalars(
            select(CrmRolePermission)
            .where(CrmRolePermission.role_id == role_id)
            .order_by(CrmRolePermission.permission_id.asc())
        ).all()
        return [self._to_domain(row) for row in rows]

    def list_by_permission_id(self, permission_id: int) -> list[CrmRolePermissionEntity]:
        rows = self.session.scalars(
            select(CrmRolePermission)
            .where(CrmRolePermission.permission_id == permission_id)
            .order_by(CrmRolePermission.role_id.asc())
        ).all()
        return [self._to_domain(row) for row in rows]


class SqlAlchemyCrmUserRoleRepository(CrmUserRoleRepositoryProtocol):
    def __init__(self, session: Session) -> None:
        self.session = session

    def _to_domain(self, row: CrmUserRole) -> CrmUserRoleEntity:
        return CrmUserRoleEntity(
            user_id=row.user_id,
            role_id=row.role_id,
            assigned_at=row.assigned_at,
        )

    def _to_row(self, entity: CrmUserRoleEntity) -> CrmUserRole:
        kwargs: dict[str, object] = {
            "user_id": entity.user_id,
            "role_id": entity.role_id,
        }
        if entity.assigned_at is not None:
            kwargs["assigned_at"] = entity.assigned_at
        return CrmUserRole(**kwargs)

    def save(self, entity: CrmUserRoleEntity) -> CrmUserRoleEntity:
        row = self.session.merge(self._to_row(entity))
        self.session.flush()
        return self._to_domain(row)

    def save_many(self, entities: list[CrmUserRoleEntity]) -> list[CrmUserRoleEntity]:
        rows = [self.session.merge(self._to_row(entity)) for entity in entities]
        self.session.flush()
        return [self._to_domain(row) for row in rows]

    def list_by_user_id(self, user_id: int) -> list[CrmUserRoleEntity]:
        rows = self.session.scalars(
            select(CrmUserRole)
            .where(CrmUserRole.user_id == user_id)
            .order_by(CrmUserRole.role_id.asc())
        ).all()
        return [self._to_domain(row) for row in rows]

    def list_by_role_id(self, role_id: int) -> list[CrmUserRoleEntity]:
        rows = self.session.scalars(
            select(CrmUserRole)
            .where(CrmUserRole.role_id == role_id)
            .order_by(CrmUserRole.user_id.asc())
        ).all()
        return [self._to_domain(row) for row in rows]
