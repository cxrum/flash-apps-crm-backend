from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.hash_protocol import HashableValue
from app.domain.pagination import Pagination
from app.domain.permission.CrmPermissionEntity import CrmPermissionEntity
from app.domain.permission.permission_repository_protocol import CrmPermissionRepositoryProtocol
from app.domain.role.CrmRoleEntity import CrmRoleEntity
from app.domain.role.role_repository_protocol import CrmRoleRepositoryProtocol
from app.domain.user.CrmUserEntity import CrmUserEntity
from app.domain.user.user_repository_protocol import CrmUserRepositoryProtocol
from app.domain.user_permissions.CrmUserPermissionEntity import CrmUserPermissionEntity
from app.domain.user_permissions.user_permissions_repository_protocol import CrmUserPermissionsRepositoryProtocol
from app.infra.db.crm.models import (
    CrmPermission,
    CrmRole,
    CrmUserPermissions,
    CrmUser,
)
from app.infra.exception import InfraGeneralException


def _apply_pagination(stmt, pagination: Pagination | None):
    if pagination is not None and pagination.offset is not None:
        stmt = stmt.offset(pagination.offset)
    if pagination is not None and pagination.limit is not None:
        stmt = stmt.limit(pagination.limit)
    return stmt


class SqlAlchemyCrmUserRepository(CrmUserRepositoryProtocol):
    def __init__(self, session: Session) -> None:
        self.session = session

    def _to_domain(self, row: CrmUser) -> CrmUserEntity:
        return CrmUserEntity(
            user_id=row.user_id,
            full_name=row.full_name,
            email=row.email,
            time_zone=row.time_zone,
            password_hash=HashableValue.from_hex(row.password_hash),
            is_active=row.is_active,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )

    def _to_row(self, entity: CrmUserEntity) -> CrmUser:
        kwargs: dict[str, object] = {
            "full_name": entity.full_name,
            "email": entity.email,
            "time_zone": entity.time_zone,
            "password_hash": entity.password_hash.to_hex(),
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

    def delete(self, user_id: int) -> CrmUserEntity:
        row = self.session.get(CrmUser, user_id)
        if row is None:
            raise InfraGeneralException()

        user = self._to_domain(row)
        self.session.delete(row)
        self.session.flush()
        return user

    def get_by_email(self, email: str) -> CrmUserEntity | None:
        row = self.session.scalars(
            select(CrmUser).where(CrmUser.email == email)
        ).first()
        return self._to_domain(row) if row is not None else None

    def list_all(self, *, pagination: Pagination | None = None) -> list[CrmUserEntity]:
        rows = self.session.scalars(
            _apply_pagination(select(CrmUser).order_by(CrmUser.user_id.asc()), pagination)
        ).all()
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

    def delete(self, role_id: int) -> CrmRoleEntity:
        row = self.session.get(CrmRole, role_id)
        if row is None:
            raise InfraGeneralException()

        role = self._to_domain(row)
        self.session.delete(row)
        self.session.flush()
        return role

    def get_by_code(self, code: str) -> CrmRoleEntity | None:
        row = self.session.scalars(select(CrmRole).where(CrmRole.code == code)).first()
        return self._to_domain(row) if row is not None else None

    def list_all(self, *, pagination: Pagination | None = None) -> list[CrmRoleEntity]:
        rows = self.session.scalars(
            _apply_pagination(select(CrmRole).order_by(CrmRole.role_id.asc()), pagination)
        ).all()
        return [self._to_domain(row) for row in rows]


class SqlAlchemyCrmPermissionRepository(CrmPermissionRepositoryProtocol):
    def __init__(self, session: Session) -> None:
        self.session = session

    @staticmethod
    def _to_domain(row: CrmPermission) -> CrmPermissionEntity:
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

    def delete(self, permission_id: int) -> CrmPermissionEntity:
        row = self.session.get(CrmPermission, permission_id)
        if row is None:
            raise InfraGeneralException()

        permission = self._to_domain(row)
        self.session.delete(row)
        self.session.flush()
        return permission

    def get_by_code(self, code: str) -> CrmPermissionEntity | None:
        row = self.session.scalars(select(CrmPermission).where(CrmPermission.code == code)).first()
        return self._to_domain(row) if row is not None else None

    def list_all(self, *, pagination: Pagination | None = None) -> list[CrmPermissionEntity]:
        rows = self.session.scalars(
            _apply_pagination(
                select(CrmPermission).order_by(CrmPermission.permission_id.asc()),
                pagination,
            )
        ).all()
        return [self._to_domain(row) for row in rows]


class SqlAlchemyCrmUserPermissionRepository(CrmUserPermissionsRepositoryProtocol):
    def __init__(self, session: Session) -> None:
        self.session = session

    def _to_domain(self, row: CrmUserPermissions) -> CrmUserPermissionEntity:
        return CrmUserPermissionEntity(
            user_id=row.user_id,
            app_id=row.app_id,
            permission_id=row.permission_id,
            assigned_at=row.assigned_at,
        )

    def _to_row(self, entity: CrmUserPermissionEntity) -> CrmUserPermissions:
        kwargs: dict[str, object] = {
            "user_id": entity.user_id,
            "app_id": entity.app_id,
            "permission_id": entity.permission_id,
        }
        if entity.assigned_at is not None:
            kwargs["assigned_at"] = entity.assigned_at
        return CrmUserPermissions(**kwargs)

    def save(self, entity: CrmUserPermissionEntity) -> CrmUserPermissionEntity:
        row = self.session.merge(self._to_row(entity))
        self.session.flush()
        return self._to_domain(row)

    def save_many(self, entities: list[CrmUserPermissionEntity]) -> list[CrmUserPermissionEntity]:
        rows = [self.session.merge(self._to_row(entity)) for entity in entities]
        self.session.flush()
        return [self._to_domain(row) for row in rows]

    def list_by_user_id(
        self,
        user_id: int,
        *,
        pagination: Pagination | None = None,
    ) -> list[CrmUserPermissionEntity]:
        rows = self.session.scalars(_apply_pagination(
            select(CrmUserPermissions)
            .where(CrmUserPermissions.user_id == user_id)
            .order_by(CrmUserPermissions.permission_id.asc()),
            pagination,
        )).all()
        return [self._to_domain(row) for row in rows]

    def list_by_permission_id(
        self,
        permission_id: int,
        *,
        pagination: Pagination | None = None,
    ) -> list[CrmUserPermissionEntity]:
        rows = self.session.scalars(_apply_pagination(
            select(CrmUserPermissions)
            .where(CrmUserPermissions.permission_id == permission_id)
            .order_by(CrmUserPermissions.user_id.asc()),
            pagination,
        )).all()
        return [self._to_domain(row) for row in rows]

    def list_by_user_id_per_app(
        self,
        user_id: int,
        app_id: int,
        *,
        pagination: Pagination | None = None,
    ) -> list[CrmPermissionEntity]:
        rows = self.session.scalars(_apply_pagination(
            select(CrmPermission)
            .join(CrmUserPermissions, CrmPermission.permission_id == CrmUserPermissions.permission_id)
            .where(CrmUserPermissions.user_id == user_id, CrmUserPermissions.app_id == app_id)
            .order_by(CrmUserPermissions.permission_id.asc()),
            pagination,
        )).all()
        return [SqlAlchemyCrmPermissionRepository._to_domain(row) for row in rows]
    
    def delete(
        self,
        user_id: int,
        permission_id: int,
        app_id: int,
    ) ->CrmUserPermissionEntity:
        row = self.session.get(CrmUserPermissions, {"user_id": user_id, "permission_id": permission_id, "app_id": app_id})
        
        if row is None:
            raise RuntimeError
        
        self.session.delete(row)
        self.session.flush()
        return self._to_domain(row)