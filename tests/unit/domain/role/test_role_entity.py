from __future__ import annotations

import pytest

from app.modules.crm.domain.role.CrmRoleEntity import Roles
from tests.unit.builders import build_role_entity


@pytest.mark.parametrize(
    ("role_code", "required_role", "expected"),
    [
        pytest.param(Roles.ADMIN.value, Roles.ADMIN, True, id="admin-meets-admin"),
        pytest.param(Roles.ADMIN.value, Roles.MANAGER, True, id="admin-meets-manager"),
        pytest.param(Roles.MANAGER.value, Roles.MANAGER, True, id="manager-meets-manager"),
        pytest.param(Roles.MANAGER.value, Roles.ADMIN, False, id="manager-does-not-meet-admin"),
        pytest.param(Roles.ADMIN.value, "manager", True, id="string-required-role-is-supported"),
        pytest.param("viewer", Roles.MANAGER, False, id="unknown-current-role-fails"),
        pytest.param(Roles.ADMIN.value, "viewer", False, id="unknown-required-role-fails"),
    ],
)
def test_compare_uses_role_hierarchy(
    role_code: str,
    required_role: Roles | str,
    expected: bool,
) -> None:
    role = build_role_entity(code=role_code)

    assert role.compare(required_role) is expected


def test_exact_role_helpers_remain_exact_matches() -> None:
    admin_role = build_role_entity(code=Roles.ADMIN.value, display_name="Admin")
    manager_role = build_role_entity(code=Roles.MANAGER.value, display_name="Manager")

    assert admin_role.is_admin_role() is True
    assert admin_role.is_manager_role() is False
    assert manager_role.is_admin_role() is False
    assert manager_role.is_manager_role() is True
