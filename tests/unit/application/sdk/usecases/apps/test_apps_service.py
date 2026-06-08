from __future__ import annotations

import pytest

from app.application.exception import GeneralException
from app.domain.role.CrmRoleEntity import Roles
from app.domain.hash_protocol import HashableValue
from tests.unit.builders import (
    build_app_entity,
    build_app_platform_entity,
    build_app_secret_entity,
    build_role_entity,
    build_sdk_application_configuration_command,
    build_sdk_create_app_command,
    build_sdk_create_app_platform_command,
    build_secret_template_entity,
    build_user_app_access_entity,
)
from tests.unit.base import UnitTestContext


def test_create_app_drafts_and_saves_app(unit_test_context: UnitTestContext) -> None:
    service = unit_test_context.build_app_service()
    admin_role = unit_test_context.uow.role_repo.save(
        build_role_entity(code=Roles.ADMIN.value, display_name="Admin")
    )

    response = service.create_app(build_sdk_create_app_command())
    assert response.app.app_id is not None

    saved_app = unit_test_context.uow.app_repo.get_by_id(response.app.app_id)

    assert saved_app is not None
    assert saved_app.status == "active"
    assert saved_app.code_slug == "test-app"
    assert saved_app.tech_description == "Technical description"
    assert admin_role.role_id is not None


def test_create_app_platform_rejects_invalid_platform(unit_test_context: UnitTestContext) -> None:
    service = unit_test_context.build_app_service()

    with pytest.raises(GeneralException, match="App platform does not valid"):
        service.create_app_platform(build_sdk_create_app_platform_command(platform="web"))


def test_create_app_platform_rejects_missing_app(unit_test_context: UnitTestContext) -> None:
    service = unit_test_context.build_app_service()
    manager_role = unit_test_context.uow.role_repo.save(
        build_role_entity(code=Roles.MANAGER.value, display_name="Manager")
    )
    unit_test_context.uow.user_app_access_repo.save(
        build_user_app_access_entity(role_id=manager_role.role_id)
    )

    with pytest.raises(GeneralException, match="App with id 1 doesn't exist"):
        service.create_app_platform(build_sdk_create_app_platform_command())


def test_create_app_platform_saves_valid_platform(unit_test_context: UnitTestContext) -> None:
    service = unit_test_context.build_app_service()
    unit_test_context.uow.app_repo.save(build_app_entity(app_id=1))
    admin_role = unit_test_context.uow.role_repo.save(
        build_role_entity(code=Roles.ADMIN.value, display_name="Admin")
    )
    unit_test_context.uow.user_app_access_repo.save(
        build_user_app_access_entity(role_id=admin_role.role_id)
    )

    response = service.create_app_platform(build_sdk_create_app_platform_command())

    assert response.app_platform.platform_id is not None
    saved_platform = unit_test_context.uow.app_platform_repo.get_by_id(response.app_platform.platform_id)

    assert saved_platform is not None
    assert saved_platform.platform == "ios"
    assert saved_platform.package_name == "com.example.test"
    expected_encrypted_secret = f"enc::{HashableValue.from_str('random-hash-32-1').to_hex()}"
    assert saved_platform.sdk_secret_encrypted == expected_encrypted_secret
    assert saved_platform.sdk_public_key == HashableValue.from_str("random-hash-8-2").to_hex()
    assert response.sdk_secret == expected_encrypted_secret
    assert response.app_platform.sdk_secret_encrypted == expected_encrypted_secret
    assert [call.method for call in unit_test_context.encryption_service.calls] == ["encrypt"]
    assert [call.method for call in unit_test_context.hash_service.calls] == ["random_hash", "random_hash"]
    assert [call.args for call in unit_test_context.hash_service.calls] == [(32,), (8,)]


def test_create_app_platform_hides_secret_for_manager(unit_test_context: UnitTestContext) -> None:
    service = unit_test_context.build_app_service()
    unit_test_context.uow.app_repo.save(build_app_entity(app_id=1))
    manager_role = unit_test_context.uow.role_repo.save(
        build_role_entity(code=Roles.MANAGER.value, display_name="Manager")
    )
    unit_test_context.uow.user_app_access_repo.save(
        build_user_app_access_entity(role_id=manager_role.role_id)
    )

    response = service.create_app_platform(build_sdk_create_app_platform_command())

    assert response.sdk_secret == "enc***"
    assert response.app_platform.sdk_secret_encrypted == "enc***"


def test_get_app_config_secrets_merges_templates_with_platform_values(
    unit_test_context: UnitTestContext,
) -> None:
    service = unit_test_context.build_app_service()
    unit_test_context.uow.app_repo.save(build_app_entity(app_id=1))
    saved_platform = unit_test_context.uow.app_platform_repo.save(
        build_app_platform_entity(app_id=1, platform="ios")
    )
    other_platform = unit_test_context.uow.app_platform_repo.save(
        build_app_platform_entity(
            app_id=1,
            platform="android",
            install_key="install-key-android",
        )
    )

    template_with_value = unit_test_context.uow.secret_template_repo.save(
        build_secret_template_entity(
            template_id=1, 
            code="api_key", 
            value_type="text",
            scope="client_public"
        )
    )
    
    template_withot_value = unit_test_context.uow.secret_template_repo.save(
        build_secret_template_entity(
            template_id=2, 
            code="something_key", 
            scope="client_public"
        )
    )
    
    template_seacret = unit_test_context.uow.secret_template_repo.save(
        build_secret_template_entity(
            template_id=3, 
            code="feature_flag", 
            value_type="text",
            scope="server_private"
        )
    )

    unit_test_context.uow.app_secret_repo.save(
        build_app_secret_entity(
            secret_id=10,
            template_id=template_with_value.template_id,
            platform_id=saved_platform.platform_id,
            encrypted_value="enc::real-secret",
            active_flag=True,
            version=2,
        )
    )
    unit_test_context.uow.app_secret_repo.save(
        build_app_secret_entity(
            secret_id=11,
            template_id=template_with_value.template_id,
            platform_id=saved_platform.platform_id,
            encrypted_value="enc::ignored-secret",
            active_flag=False,
            version=3,
        )
    )
    unit_test_context.uow.app_secret_repo.save(
        build_app_secret_entity(
            secret_id=12,
            template_id=template_seacret.template_id,
            platform_id=other_platform.platform_id,
            encrypted_value="enc::other-platform-secret",
            active_flag=True,
            version=1,
        )
    )    
    unit_test_context.uow.app_secret_repo.save(
        build_app_secret_entity(
            secret_id=13,
            template_id=template_withot_value.template_id,
            platform_id=other_platform.platform_id,
            encrypted_value="enc::other-platform-secret",
            active_flag=True,
            version=1,
        )
    )

    response = service.get_app_config_secrets(
        build_sdk_application_configuration_command(install_key=saved_platform.install_key)
    )

    by_code = {
        item.code: item.value
        for item in response.platform_configurations
    }
    assert by_code == {"api_key": "real-secret"}
    assert [call.method for call in unit_test_context.encryption_service.calls] == ["decrypt"]
