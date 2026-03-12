from __future__ import annotations

import pytest

from app.application.exceptions import ApplicationError
from tests.unit.builders import (
    build_app_entity,
    build_app_platform_entity,
    build_app_secret_entity,
    build_sdk_application_configuration_command,
    build_sdk_create_app_command,
    build_sdk_create_app_platform_command,
    build_secret_template_entity,
)
from tests.unit.base import UnitTestContext


def test_create_app_drafts_and_saves_app(unit_test_context: UnitTestContext) -> None:
    service = unit_test_context.build_app_service()

    response = service.create_app(build_sdk_create_app_command())
    saved_app = unit_test_context.uow.app_repo.get_by_id(response.app_id)

    assert saved_app is not None
    assert saved_app.status == "draft"
    assert saved_app.code_slug == "test-app"


def test_create_platform_rejects_invalid_platform(unit_test_context: UnitTestContext) -> None:
    service = unit_test_context.build_app_service()

    with pytest.raises(ApplicationError, match="App platform does not valid"):
        service.create_platform(build_sdk_create_app_platform_command(platform="web"))


def test_create_platform_rejects_missing_app(unit_test_context: UnitTestContext) -> None:
    service = unit_test_context.build_app_service()

    with pytest.raises(ApplicationError, match="App with id 1 doesnt exist"):
        service.create_platform(build_sdk_create_app_platform_command())


def test_create_platform_saves_valid_platform(unit_test_context: UnitTestContext) -> None:
    service = unit_test_context.build_app_service()
    unit_test_context.uow.app_repo.save(build_app_entity(app_id=1))

    response = service.create_platform(build_sdk_create_app_platform_command())
    saved_platform = unit_test_context.uow.app_platform_repo.get_by_id(response.platform_id)

    assert saved_platform is not None
    assert saved_platform.platform == "ios"
    assert saved_platform.package_name == "com.example.test"


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
        build_sdk_application_configuration_command(app_id=1, platform="ios")
    )

    by_code = {
        item.template.code: item
        for item in response.platform_configurations
    }
    assert set(by_code) == {"api_key", "something_key"}
    assert "feature_flag" not in set(by_code)
    assert by_code["api_key"].value == "real-secret"
    assert by_code["api_key"].template.version == 2.0
    assert by_code["api_key"].template.is_active is True
    assert by_code["something_key"].value is None
    assert by_code["something_key"].template.is_active is False
    assert [call.method for call in unit_test_context.encryption_service.calls] == ["decrypt"]
