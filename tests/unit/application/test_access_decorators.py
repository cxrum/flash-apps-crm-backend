from __future__ import annotations

from dataclasses import dataclass

import pytest

from app.modules.crm.application.access_decorators import require_app_access, require_permission, require_role
from app.modules.crm.application.admin.crm_authorization.exceptions import AuthorizationException
from app.modules.crm.application.admin.crm_authorization.service import CrmAuthorizationService
from app.modules.crm.domain.permission.CrmPermissionEntity import CrmPermissionEntity
from app.modules.crm.domain.role.CrmRoleEntity import Roles
from app.modules.crm.domain.role.exceptions import ManagerAccessRequired
from app.modules.crm.domain.user_permissions.CrmUserPermissionEntity import CrmUserPermissionEntity
from tests.unit.builders import (
    build_permission_entity,
    build_role_entity,
    build_sdk_create_app_platform_command,
    build_user_app_access_entity,
)
from tests.unit.doubles.domain.uow import StubUnitOfWork, StubUoWFactory


@dataclass
class _CommandWithoutAppId:
    crm_user_id: int = 1


class _DecoratedService:
    def __init__(self, uow: StubUnitOfWork) -> None:
        self._uow_factory = StubUoWFactory(uow)
        self._authorization_service = CrmAuthorizationService(self._uow_factory)
        self.calls = 0

    @require_app_access()
    def inspect_access(self, command):
        with self._uow_factory.create():
            self.calls += 1
            return "ok"

    @require_role(Roles.ADMIN)
    def admin_only(self, command):
        self.calls += 1
        return "admin"

    @require_permission(CrmPermissionEntity.manage_push_permission())
    def permission_only(self, command):
        with self._uow_factory.create():
            self.calls += 1
            return "permission"

    def _resolve_missing_app_context(_service, _uow, command):
        return command.crm_user_id, 1

    @require_permission(
        CrmPermissionEntity.manage_push_permission(),
        context_resolver=_resolve_missing_app_context,
    )
    def permission_with_resolved_app(self, command):
        with self._uow_factory.create():
            self.calls += 1
            return "resolved"


def test_require_app_access_calls_wrapped_method_after_check() -> None:
    uow = StubUnitOfWork()
    manager_role = uow.role_repo.save(build_role_entity(code=Roles.MANAGER.value, display_name="Manager"))
    uow.user_app_access_repo.save(build_user_app_access_entity(role_id=manager_role.role_id))
    service = _DecoratedService(uow)

    result = service.inspect_access(build_sdk_create_app_platform_command())

    assert result == "ok"
    assert service.calls == 1


def test_require_role_rejects_insufficient_role() -> None:
    uow = StubUnitOfWork()
    manager_role = uow.role_repo.save(build_role_entity(code=Roles.MANAGER.value, display_name="Manager"))
    uow.user_app_access_repo.save(build_user_app_access_entity(role_id=manager_role.role_id))
    service = _DecoratedService(uow)

    with pytest.raises(ManagerAccessRequired):
        service.admin_only(build_sdk_create_app_platform_command())

    assert service.calls == 0


def test_require_permission_calls_wrapped_method_after_check() -> None:
    uow = StubUnitOfWork()
    manager_role = uow.role_repo.save(build_role_entity(code=Roles.MANAGER.value, display_name="Manager"))
    permission = uow.permission_repo.save(build_permission_entity(code=CrmPermissionEntity.manage_push_permission()))
    assert permission.permission_id is not None
    uow.user_app_access_repo.save(build_user_app_access_entity(role_id=manager_role.role_id))
    uow.user_permissions_repo.save(
        CrmUserPermissionEntity(
            user_id=1,
            app_id=1,
            permission_id=permission.permission_id,
        )
    )
    service = _DecoratedService(uow)

    result = service.permission_only(build_sdk_create_app_platform_command())

    assert result == "permission"
    assert service.calls == 1


def test_require_permission_rejects_missing_permission() -> None:
    uow = StubUnitOfWork()
    manager_role = uow.role_repo.save(build_role_entity(code=Roles.MANAGER.value, display_name="Manager"))
    uow.user_app_access_repo.save(build_user_app_access_entity(role_id=manager_role.role_id))
    service = _DecoratedService(uow)

    with pytest.raises(AuthorizationException):
        service.permission_only(build_sdk_create_app_platform_command())

    assert service.calls == 0


def test_require_permission_supports_context_resolver() -> None:
    uow = StubUnitOfWork()
    manager_role = uow.role_repo.save(build_role_entity(code=Roles.MANAGER.value, display_name="Manager"))
    permission = uow.permission_repo.save(build_permission_entity(code=CrmPermissionEntity.manage_push_permission()))
    assert permission.permission_id is not None
    uow.user_app_access_repo.save(build_user_app_access_entity(role_id=manager_role.role_id))
    uow.user_permissions_repo.save(
        CrmUserPermissionEntity(
            user_id=1,
            app_id=1,
            permission_id=permission.permission_id,
        )
    )
    service = _DecoratedService(uow)

    result = service.permission_with_resolved_app(_CommandWithoutAppId())

    assert result == "resolved"
    assert service.calls == 1
