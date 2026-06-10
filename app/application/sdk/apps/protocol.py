from typing import Protocol

from app.application.sdk.apps.commands import (
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
from app.application.sdk.apps.responses import (
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


class AppServiceProtocol(Protocol):
    def get_app(self, command: GetAppCommand) -> GetAppResponse: ...
    def get_apps(self, command: ListAppsCommand) -> AppListResponse: ...

    def rotate_platform_secret(
        self,
        command: RotatePlatformSecretCommand,
    ) -> RotatePlatformSecretResponse: ...

    def create_app(self, command: CreateAppCommand) -> CreateAppResponse: ...
    def update_app(self, command: UpdateAppCommand) -> UpdateAppResponse: ...
    def delete_app(self, command: DeleteAppCommand) -> DeleteAppResponse: ...

    def get_app_platforms(
        self,
        command: ListAppPlatformsCommand,
    ) -> ListAppPlatformsResponse: ...

    def create_app_platform(
        self,
        command: CreateAppPlatformCommand,
    ) -> CreatePlatformResponse: ...

    def get_app_platform(self, command: GetAppPlatformCommand) -> GetPlatformResponse: ...

    def update_app_platform(
        self,
        command: UpdateAppPlatformCommand,
    ) -> UpdatePlatformResponse: ...

    def delete_app_platform(
        self,
        command: DeleteAppPlatformCommand,
    ) -> DeletePlatformResponse: ...

    def get_app_config_secrets(
        self,
        command: AppConfigurationCommand,
    ) -> AppConfigQueryResponse: ...
