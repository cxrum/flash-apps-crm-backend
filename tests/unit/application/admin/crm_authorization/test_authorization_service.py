from __future__ import annotations

from app.modules.crm.application.admin.crm_authorization.service import CrmAuthorizationService
from app.modules.crm.domain.permission.CrmPermissionEntity import CrmPermissionEntity
from app.modules.crm.domain.role.CrmRoleEntity import Roles
from app.modules.crm.domain.user_permissions.CrmUserPermissionEntity import CrmUserPermissionEntity
from tests.unit.builders import (
    build_permission_entity,
    build_role_entity,
    build_user_app_access_entity,
)
from tests.unit.doubles.domain.uow import StubUnitOfWork, StubUoWFactory


def test_is_user_manager_permission_access_allows_admin_role() -> None:
    uow = StubUnitOfWork()
    service = CrmAuthorizationService(StubUoWFactory(uow))
    admin_role = uow.role_repo.save(build_role_entity(code=Roles.ADMIN.value, display_name="Admin"))
    assert admin_role.role_id is not None
    uow.user_app_access_repo.save(build_user_app_access_entity(user_id=1, app_id=7, role_id=admin_role.role_id))

    assert service.is_user_manager_permission_access(crm_user_id=1, app_id=7) is True


def test_is_user_admin_permission_access_returns_boolean_true_for_admin() -> None:
    uow = StubUnitOfWork()
    service = CrmAuthorizationService(StubUoWFactory(uow))
    admin_role = uow.role_repo.save(build_role_entity(code=Roles.ADMIN.value, display_name="Admin"))
    assert admin_role.role_id is not None
    uow.user_app_access_repo.save(build_user_app_access_entity(user_id=2, app_id=8, role_id=admin_role.role_id))

    assert service.is_user_admin_permission_access(crm_user_id=2, app_id=8) is True


def test_is_user_permission_access_returns_true_for_assigned_permission() -> None:
    uow = StubUnitOfWork()
    service = CrmAuthorizationService(StubUoWFactory(uow))
    manager_role = uow.role_repo.save(build_role_entity(code=Roles.MANAGER.value, display_name="Manager"))
    permission = uow.permission_repo.save(build_permission_entity(code=CrmPermissionEntity.manage_push_permission()))
    assert permission.permission_id is not None
    uow.user_app_access_repo.save(build_user_app_access_entity(user_id=3, app_id=9, role_id=manager_role.role_id))
    uow.user_permissions_repo.save(
        CrmUserPermissionEntity(
            user_id=3,
            app_id=9,
            permission_id=permission.permission_id,
        )
    )

    assert (
        service.is_user_permission_access(
            crm_user_id=3,
            app_id=9,
            permission_code=CrmPermissionEntity.manage_push_permission(),
        )
        is True
    )


def test_is_user_permission_access_allows_admin_without_explicit_permission() -> None:
    uow = StubUnitOfWork()
    service = CrmAuthorizationService(StubUoWFactory(uow))
    admin_role = uow.role_repo.save(build_role_entity(code=Roles.ADMIN.value, display_name="Admin"))
    uow.user_app_access_repo.save(build_user_app_access_entity(user_id=4, app_id=10, role_id=admin_role.role_id))

    assert (
        service.is_user_permission_access(
            crm_user_id=4,
            app_id=10,
            permission_code=CrmPermissionEntity.view_raw_logs_permission(),
        )
        is True
    )
