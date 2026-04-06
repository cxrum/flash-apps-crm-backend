from __future__ import annotations

from app.application.admin.crm_authorization.service import CrmAuthorizationService
from app.domain.role.CrmRoleEntity import Roles
from tests.unit.builders import build_role_entity, build_user_app_access_entity
from tests.unit.doubles.domain.uow import StubUoWFactory, StubUnitOfWork


def test_is_user_manager_permission_access_allows_admin_role() -> None:
    uow = StubUnitOfWork()
    service = CrmAuthorizationService(StubUoWFactory(uow))
    admin_role = uow.role_repo.save(
        build_role_entity(code=Roles.ADMIN.value, display_name="Admin")
    )
    assert admin_role.role_id is not None
    uow.user_app_access_repo.save(
        build_user_app_access_entity(user_id=1, app_id=7, role_id=admin_role.role_id)
    )

    assert service.is_user_manager_permission_access(crm_user_id=1, app_id=7) is True


def test_is_user_admin_permission_access_returns_boolean_true_for_admin() -> None:
    uow = StubUnitOfWork()
    service = CrmAuthorizationService(StubUoWFactory(uow))
    admin_role = uow.role_repo.save(
        build_role_entity(code=Roles.ADMIN.value, display_name="Admin")
    )
    assert admin_role.role_id is not None
    uow.user_app_access_repo.save(
        build_user_app_access_entity(user_id=2, app_id=8, role_id=admin_role.role_id)
    )

    assert service.is_user_admin_permission_access(crm_user_id=2, app_id=8) is True
