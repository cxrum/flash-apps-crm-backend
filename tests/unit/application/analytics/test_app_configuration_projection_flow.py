from __future__ import annotations

import asyncio

import pytest

from app.modules.analytics.domain.app.AnalyticsAppEntity import AnalyticsAppEntity
from app.modules.analytics.domain.app_platform.AnalyticsAppPlatformEntity import AnalyticsAppPlatformEntity
from app.core.bus.event.events.app_configuration import (
    AppConfigurationProjectionMessage,
    AppPlatformConfigurationProjectionMessage,
)
from app.core.bus.type import EventMessage
from app.modules.analytics.core.exception import AnalyticsApplicationException
from app.modules.analytics.handlers.app.projection import (
    AppConfigurationProjectionHandler,
    AppPlatformConfigurationProjectionHandler,
)
from app.modules.crm.application.admin.crm_authorization.service import CrmAuthorizationService
from app.modules.crm.application.sdk.apps.commands import UpdateAppCommand, UpdateAppPlatformCommand
from app.modules.crm.application.sdk.apps.service import AppService
from app.modules.crm.infra.event_bus.async_bus.in_memory import InMemoryAsyncEventBus
from app.modules.crm.domain.role.CrmRoleEntity import Roles
from tests.unit.base import UnitTestContext
from tests.unit.builders import (
    build_role_entity,
    build_sdk_create_app_command,
    build_sdk_create_app_platform_command,
)
from tests.unit.doubles.domain.uow import StubUnitOfWork, StubUoWFactory


class _AnalyticsAppRepository:
    def __init__(self) -> None:
        self._items: dict[int, AnalyticsAppEntity] = {}
        self.saved = asyncio.Event()

    def save(self, entity: AnalyticsAppEntity) -> AnalyticsAppEntity:
        assert entity.app_id is not None
        self._items[entity.app_id] = entity
        self.saved.set()
        return entity

    def get_by_id(self, app_id: int) -> AnalyticsAppEntity | None:
        return self._items.get(app_id)


class _AnalyticsAppPlatformRepository:
    def __init__(self) -> None:
        self._items: dict[int, AnalyticsAppPlatformEntity] = {}
        self.saved = asyncio.Event()

    def save(self, entity: AnalyticsAppPlatformEntity) -> AnalyticsAppPlatformEntity:
        assert entity.platform_id is not None
        self._items[entity.platform_id] = entity
        self.saved.set()
        return entity

    def get_by_id(self, platform_id: int) -> AnalyticsAppPlatformEntity | None:
        return self._items.get(platform_id)


def _build_app_service(unit_test_context: UnitTestContext, event_bus: InMemoryAsyncEventBus) -> AppService:
    return AppService(
        uow_factory=unit_test_context.uow_factory,
        event_bus=event_bus,
        authorization_service=CrmAuthorizationService(unit_test_context.uow_factory),
        encryption_service=unit_test_context.encryption_service,
        hash_service=unit_test_context.hash_service,
    )


def _build_projection_bus() -> tuple[InMemoryAsyncEventBus, _AnalyticsAppRepository, _AnalyticsAppPlatformRepository]:
    app_repo = _AnalyticsAppRepository()
    platform_repo = _AnalyticsAppPlatformRepository()
    analytics_uow = StubUnitOfWork(app_repo=app_repo, app_platform_repo=platform_repo)
    event_bus = InMemoryAsyncEventBus()
    event_bus.subscribe(
        AppConfigurationProjectionMessage.EVENT_NAME,
        AppConfigurationProjectionHandler(StubUoWFactory(analytics_uow)),  # type: ignore[arg-type]
    )
    event_bus.subscribe(
        AppPlatformConfigurationProjectionMessage.EVENT_NAME,
        AppPlatformConfigurationProjectionHandler(StubUoWFactory(analytics_uow)),  # type: ignore[arg-type]
    )
    return event_bus, app_repo, platform_repo


def test_app_service_create_events_populate_analytics_configuration_projections(
    unit_test_context: UnitTestContext,
) -> None:
    async def scenario() -> None:
        event_bus, app_repo, platform_repo = _build_projection_bus()
        service = _build_app_service(unit_test_context, event_bus)
        unit_test_context.uow.role_repo.save(
            build_role_entity(code=Roles.ADMIN.value, display_name="Admin")
        )

        await event_bus.start()
        try:
            app = service.create_app(
                build_sdk_create_app_command(code_slug="analytics-store")
            )
            await app_repo.saved.wait()

            platform = service.create_app_platform(
                build_sdk_create_app_platform_command(
                    app_id=app.app.app_id,
                    platform="android",
                    install_key="android-install-key",
                )
            )
            await platform_repo.saved.wait()
        finally:
            await event_bus.stop()

        assert app.app.app_id is not None
        assert platform.app_platform.platform_id is not None
        assert app_repo.get_by_id(app.app.app_id) == AnalyticsAppEntity(
            app_id=app.app.app_id,
            code_slug="analytics-store",
        )
        assert platform_repo.get_by_id(platform.app_platform.platform_id) == AnalyticsAppPlatformEntity(
            platform_id=platform.app_platform.platform_id,
            app_id=app.app.app_id,
            platform="android",
            install_key="android-install-key",
            sdk_secret_encrypted=platform.app_platform.sdk_secret_encrypted,
        )

    asyncio.run(scenario())


def test_app_service_update_events_replace_existing_analytics_configuration(
    unit_test_context: UnitTestContext,
) -> None:
    async def scenario() -> None:
        event_bus, app_repo, platform_repo = _build_projection_bus()
        service = _build_app_service(unit_test_context, event_bus)
        unit_test_context.uow.role_repo.save(
            build_role_entity(code=Roles.ADMIN.value, display_name="Admin")
        )

        await event_bus.start()
        try:
            app = service.create_app(build_sdk_create_app_command(code_slug="before-update"))
            await app_repo.saved.wait()
            platform = service.create_app_platform(
                build_sdk_create_app_platform_command(app_id=app.app.app_id)
            )
            await platform_repo.saved.wait()

            app_repo.saved.clear()
            platform_repo.saved.clear()
            service.update_app(
                UpdateAppCommand(
                    crm_user_id=1,
                    app_id=app.app.app_id,
                    code="after-update",
                )
            )
            service.update_app_platform(
                UpdateAppPlatformCommand(
                    crm_user_id=1,
                    app_id=app.app.app_id,
                    platform_id=platform.app_platform.platform_id,
                    package_name="com.example.updated",
                    install_key="updated-install-key",
                )
            )
            await app_repo.saved.wait()
            await platform_repo.saved.wait()
        finally:
            await event_bus.stop()

        assert app.app.app_id is not None
        assert platform.app_platform.platform_id is not None
        assert app_repo.get_by_id(app.app.app_id) == AnalyticsAppEntity(
            app_id=app.app.app_id,
            code_slug="after-update",
        )
        projected_platform = platform_repo.get_by_id(platform.app_platform.platform_id)
        assert projected_platform is not None
        assert projected_platform.install_key == "updated-install-key"
        assert projected_platform.platform == "ios"

    asyncio.run(scenario())


def test_projection_handler_rejects_a_message_for_another_projection_type() -> None:
    async def scenario() -> None:
        app_repo = _AnalyticsAppRepository()
        analytics_uow = StubUnitOfWork(app_repo=app_repo)
        handler = AppConfigurationProjectionHandler(StubUoWFactory(analytics_uow))  # type: ignore[arg-type]

        with pytest.raises(AnalyticsApplicationException) as error:
            await handler.handle(EventMessage(name=AppPlatformConfigurationProjectionMessage.EVENT_NAME))

        assert error.value.message_key == "analytics.projection.app.message.invalid"
        assert app_repo.get_by_id(1) is None

    asyncio.run(scenario())
