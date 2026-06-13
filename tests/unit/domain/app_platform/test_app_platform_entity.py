from __future__ import annotations

from app.modules.crm.domain.role.CrmRoleEntity import Roles
from tests.unit.builders import build_app_platform_entity


def test_secret_view_for_role_returns_encrypted_value_for_admin() -> None:
    platform = build_app_platform_entity(sdk_secret_encrypted="enc::secret-value")

    assert platform.secret_view_for_role(Roles.ADMIN) == "enc::secret-value"


def test_secret_view_for_role_returns_hidden_value_for_manager() -> None:
    platform = build_app_platform_entity(sdk_secret_encrypted="enc::secret-value")

    assert platform.secret_view_for_role(Roles.MANAGER) == "enc***"
