from __future__ import annotations

from app.core.bus.contract import IAsyncEventBus
from app.modules.crm.application.audited.utils import AuditConfig, AuditedUtils, AuditSnapshot
from app.modules.crm.application.exception import AppNotFound, PlatformNotFound
from app.modules.crm.application.sdk.apps.commands import (
    AppConfigurationCommand,
    CreateAppCommand,
    CreateAppPlatformCommand,
    DeleteAppCommand,
    DeleteAppPlatformCommand,
    GetAppCommand,
    GetAppPlatformCommand,
    ListAppPlatformsCommand,
    ListAppsCommand,
    RotatePlatformSecretCommand,
    UpdateAppCommand,
    UpdateAppPlatformCommand,
)
from app.modules.crm.application.sdk.apps.protocol import AppServiceProtocol
from app.modules.crm.application.sdk.apps.responses import (
    AppConfigQueryResponse,
    AppListResponse,
    CreateAppResponse,
    CreatePlatformResponse,
    DeleteAppResponse,
    DeletePlatformResponse,
    GetAppResponse,
    GetPlatformResponse,
    ListAppPlatformsResponse,
    RotatePlatformSecretResponse,
    UpdateAppResponse,
    UpdatePlatformResponse,
)
from app.modules.crm.domain.uow import UnitOfWorkFactoryProtocol


class AuditedAppsService(AppServiceProtocol):
    APP_ENTITY = "crm_apps"
    APP_PLATFORM_ENTITY = "crm_app_platforms"

    def __init__(
        self,
        uow_factory: UnitOfWorkFactoryProtocol,
        apps_service: AppServiceProtocol,
        event_bus: IAsyncEventBus,
    ) -> None:
        self.__uow_factory = uow_factory
        self.__apps_service = apps_service
        self.__async_event_bus = event_bus
        self.__audit_config = AuditConfig()

    def get_app(self, command: GetAppCommand) -> GetAppResponse:
        return self.__apps_service.get_app(command)

    def get_apps(self, command: ListAppsCommand) -> AppListResponse:
        return self.__apps_service.get_apps(command)

    def rotate_platform_secret(
        self,
        command: RotatePlatformSecretCommand,
    ) -> RotatePlatformSecretResponse:
        return AuditedUtils.audit_entity_update(
            self.__uow_factory,
            self.__async_event_bus,
            crm_user_id=command.crm_user_id,
            app_id=command.app_id,
            entity_changed=self.APP_ENTITY,
            entity_id=command.platform_id,
            loader=lambda uow: uow.app_platform_repo.get_by_id(command.platform_id),
            operation=lambda: self.__apps_service.rotate_platform_secret(command),
            ignore_fields=self.__audit_config.ignore_fields,
        )

    def create_app(self, command: CreateAppCommand) -> CreateAppResponse:
        saved_app = self.__apps_service.create_app(command)
        with self.__uow_factory.create() as uow:
            app_value = uow.app_repo.get_by_id(saved_app.app.app_id)
            if app_value is None or app_value.app_id is None:
                raise AppNotFound()

        AuditedUtils.publish_entity_change(
            async_event_bus=self.__async_event_bus,
            crm_user_id=command.crm_user_id,
            entity_changed=self.APP_ENTITY,
            app_id=app_value.app_id,
            entity_id=app_value.app_id,
            old_snapshot=AuditSnapshot(value={}, updated_at=None),
            new_snapshot=AuditSnapshot(
                value=AuditedUtils.audit_entity_value(app_value), updated_at=app_value.created_at
            ),
        )

        return saved_app

    def update_app(self, command: UpdateAppCommand) -> UpdateAppResponse:
        return AuditedUtils.audit_entity_update(
            self.__uow_factory,
            self.__async_event_bus,
            crm_user_id=command.crm_user_id,
            app_id=command.app_id,
            entity_changed=self.APP_ENTITY,
            entity_id=command.app_id,
            loader=lambda uow: uow.app_repo.get_by_id(command.app_id),
            operation=lambda: self.__apps_service.update_app(command),
            ignore_fields=self.__audit_config.ignore_fields,
        )

    def delete_app(self, command: DeleteAppCommand) -> DeleteAppResponse:
        with self.__uow_factory.create() as uow:
            app_value = uow.app_repo.get_by_id(command.app_id)
            if app_value is None or app_value.app_id is None:
                raise AppNotFound()

        deleted_app = self.__apps_service.delete_app(command)

        AuditedUtils.publish_entity_change(
            async_event_bus=self.__async_event_bus,
            crm_user_id=command.crm_user_id,
            entity_changed=self.APP_ENTITY,
            app_id=app_value.app_id,
            entity_id=app_value.app_id,
            old_snapshot=AuditSnapshot(
                value=AuditedUtils.audit_entity_value(app_value), updated_at=app_value.updated_at
            ),
            new_snapshot=AuditSnapshot(value={}, updated_at=None),
        )

        return deleted_app

    def get_app_platforms(
        self,
        command: ListAppPlatformsCommand,
    ) -> ListAppPlatformsResponse:
        return self.__apps_service.get_app_platforms(command)

    def create_app_platform(
        self,
        command: CreateAppPlatformCommand,
    ) -> CreatePlatformResponse:
        saved_platform = self.__apps_service.create_app_platform(command)
        with self.__uow_factory.create() as uow:
            platform_value = uow.app_platform_repo.get_by_id(saved_platform.app_platform.platform_id)
            if platform_value is None or platform_value.app_id is None:
                raise PlatformNotFound()

        AuditedUtils.publish_entity_change(
            async_event_bus=self.__async_event_bus,
            crm_user_id=command.crm_user_id,
            entity_changed=self.APP_PLATFORM_ENTITY,
            app_id=platform_value.app_id,
            entity_id=platform_value.app_id,
            old_snapshot=AuditSnapshot(value={}, updated_at=None),
            new_snapshot=AuditSnapshot(
                value=AuditedUtils.audit_entity_value(platform_value), updated_at=platform_value.created_at
            ),
        )

        return saved_platform

    def get_app_platform(self, command: GetAppPlatformCommand) -> GetPlatformResponse:
        return self.__apps_service.get_app_platform(command)

    def update_app_platform(
        self,
        command: UpdateAppPlatformCommand,
    ) -> UpdatePlatformResponse:
        return AuditedUtils.audit_entity_update(
            self.__uow_factory,
            self.__async_event_bus,
            crm_user_id=command.crm_user_id,
            app_id=command.app_id,
            entity_changed=self.APP_PLATFORM_ENTITY,
            entity_id=command.platform_id,
            loader=lambda uow: uow.app_platform_repo.get_by_id(command.platform_id),
            operation=lambda: self.__apps_service.update_app_platform(command),
            ignore_fields=self.__audit_config.ignore_fields,
        )

    def delete_app_platform(
        self,
        command: DeleteAppPlatformCommand,
    ) -> DeletePlatformResponse:
        with self.__uow_factory.create() as uow:
            platform_value = uow.app_platform_repo.get_by_id(command.platform_id)
            if platform_value is None or platform_value.platform_id is None:
                raise PlatformNotFound()

        deleted_platform = self.__apps_service.delete_app_platform(command)

        AuditedUtils.publish_entity_change(
            async_event_bus=self.__async_event_bus,
            crm_user_id=command.crm_user_id,
            entity_changed=self.APP_PLATFORM_ENTITY,
            app_id=platform_value.app_id,
            entity_id=platform_value.platform_id,
            old_snapshot=AuditSnapshot(
                value=AuditedUtils.audit_entity_value(platform_value),
                updated_at=platform_value.updated_at,
            ),
            new_snapshot=AuditSnapshot(value={}, updated_at=None),
        )

        return deleted_platform

    def get_app_config_secrets(
        self,
        command: AppConfigurationCommand,
    ) -> AppConfigQueryResponse:
        return self.__apps_service.get_app_config_secrets(command)
