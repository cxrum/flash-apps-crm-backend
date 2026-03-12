from __future__ import annotations

import pytest

from app.application.exceptions import ApplicationLevelError
from app.domain.app_platform.CrmAppPlatformEntity import CrmAppPlatformEntity
from tests.unit.builders import (
    build_app_entity,
    build_app_platform_entity,
    build_click_entity,
    build_sdk_install_command,
)
from tests.unit.base import UnitTestContext


def _seed_platform(
    unit_test_context: UnitTestContext,
    *,
    app_id: int = 1,
    platform: str = "ios",
    install_key: str = "install-key-ios",
) -> CrmAppPlatformEntity:
    unit_test_context.uow.app_repo.save(build_app_entity(app_id=app_id))
    return unit_test_context.uow.app_platform_repo.save(
        build_app_platform_entity(
            app_id=app_id,
            platform=platform,
            install_key=install_key,
        )
    )


def test_process_install_raises_for_unknown_install_key(
    unit_test_context: UnitTestContext,
) -> None:
    service = unit_test_context.build_ingestion_service()

    with pytest.raises(ApplicationLevelError, match="Unknown install_key"):
        service.process_install(build_sdk_install_command(install_key="missing-install-key"))


def test_process_install_creates_click_install_and_raw_event_on_first_install(
    unit_test_context: UnitTestContext,
) -> None:
    service = unit_test_context.build_ingestion_service()
    platform = _seed_platform(unit_test_context)
    command = build_sdk_install_command(click_id=None, install_key=platform.install_key)

    response = service.process_install(command)

    saved_click = unit_test_context.uow.click_repo.get_by_id(response.click_id)
    saved_install = unit_test_context.uow.install_repo.get_by_click_id(response.click_id)
    saved_events = unit_test_context.uow.event_repo.list_by_app_id(platform.app_id)

    assert response.click_id == "install-idempotency-1"
    assert saved_click is not None
    assert saved_click.app_platform_id == platform.platform_id
    assert saved_click.source == "sdk_install"
    assert saved_install is not None
    assert saved_install.app_platform_id == platform.platform_id
    assert saved_install.app_user_id is None
    assert saved_install.device_data["os_name"] == command.device.os_name
    assert [event.event_key for event in saved_events] == ["install"]
    assert saved_events[0].payload["install_key"] == command.install_key
    assert saved_events[0].click_id == response.click_id


def test_process_install_reuses_existing_redirect_click(
    unit_test_context: UnitTestContext,
) -> None:
    service = unit_test_context.build_ingestion_service()
    platform = _seed_platform(unit_test_context)
    existing_click = unit_test_context.uow.click_repo.insert(
        build_click_entity(
            click_id="redirect-click-1",
            app_platform_id=platform.platform_id or 0,
        )
    )

    response = service.process_install(
        build_sdk_install_command(
            install_key=platform.install_key,
            click_id=existing_click.click_id,
            idempotency_key="install-idempotency-2",
        )
    )

    platform_clicks = unit_test_context.uow.click_repo.list_by_platform_id(platform.platform_id or 0)
    saved_install = unit_test_context.uow.install_repo.get_by_click_id(existing_click.click_id)

    assert response.click_id == existing_click.click_id
    assert [click.click_id for click in platform_clicks] == ["redirect-click-1"]
    assert saved_install is not None
    assert saved_install.click_id == existing_click.click_id


def test_process_install_routes_to_platform_resolved_by_install_key(
    unit_test_context: UnitTestContext,
) -> None:
    service = unit_test_context.build_ingestion_service()
    unit_test_context.uow.app_repo.save(build_app_entity(app_id=1))
    ios_platform = unit_test_context.uow.app_platform_repo.save(
        build_app_platform_entity(
            app_id=1,
            platform="ios",
            install_key="install-key-ios",
        )
    )
    android_platform = unit_test_context.uow.app_platform_repo.save(
        build_app_platform_entity(
            app_id=1,
            platform="android",
            install_key="install-key-android",
        )
    )

    ios_response = service.process_install(
        build_sdk_install_command(
            click_id=None,
            install_key=ios_platform.install_key,
            idempotency_key="ios-install-1",
        )
    )
    android_response = service.process_install(
        build_sdk_install_command(
            click_id=None,
            install_key=android_platform.install_key,
            idempotency_key="android-install-1",
        )
    )

    ios_click = unit_test_context.uow.click_repo.get_by_id(ios_response.click_id)
    android_click = unit_test_context.uow.click_repo.get_by_id(android_response.click_id)

    assert ios_click is not None
    assert ios_click.app_platform_id == ios_platform.platform_id
    assert android_click is not None
    assert android_click.app_platform_id == android_platform.platform_id
    assert len(unit_test_context.uow.event_repo.list_by_app_id(1)) == 2


def test_process_install_rejects_click_bound_to_another_platform(
    unit_test_context: UnitTestContext,
) -> None:
    service = unit_test_context.build_ingestion_service()
    unit_test_context.uow.app_repo.save(build_app_entity(app_id=1))
    ios_platform = unit_test_context.uow.app_platform_repo.save(
        build_app_platform_entity(app_id=1, platform="ios", install_key="install-key-ios")
    )
    android_platform = unit_test_context.uow.app_platform_repo.save(
        build_app_platform_entity(
            app_id=1,
            platform="android",
            install_key="install-key-android",
        )
    )
    unit_test_context.uow.click_repo.insert(
        build_click_entity(
            click_id="redirect-click-1",
            app_platform_id=ios_platform.platform_id or 0,
        )
    )

    with pytest.raises(ApplicationLevelError, match="belongs to another platform"):
        service.process_install(
            build_sdk_install_command(
                install_key=android_platform.install_key,
                click_id="redirect-click-1",
                idempotency_key="install-idempotency-3",
            )
        )
