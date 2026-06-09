from pydantic import Field

from app.application.base import FlexibleCommand, PaginationCommand


class GetAppsCommand(FlexibleCommand):
    crm_user_id: int


class DeleteAppPlatformCommand(FlexibleCommand):
    crm_user_id: int
    app_id: int
    platform_id: int


class UpdateAppPlatformCommand(FlexibleCommand):
    crm_user_id: int
    app_id: int
    platform_id: int
    package_name: str
    install_key: str
    store_url: str | None = None
    status: str = "active"


class ListAppsCommand(PaginationCommand):
    crm_user_id: int


class CreateAppCommand(FlexibleCommand):
    crm_user_id: int
    name: str
    code_slug: str
    description: str | None = None
    tech_description: str | None = None
    logo_url: str | None = None
    screenshots: list[str] = Field(default_factory=list)


class RotatePlatformSecretCommand(FlexibleCommand):
    crm_user_id: int
    app_id: int
    platform_id: int


class GetAppCommand(FlexibleCommand):
    crm_user_id: int
    app_id: int


class UpdateAppCommand(FlexibleCommand):
    crm_user_id: int
    app_id: int
    code: str | None = None
    name: str | None = None
    description: str | None = None
    status: str | None = None


class DeleteAppCommand(FlexibleCommand):
    crm_user_id: int
    app_id: int


class ListAppPlatformsCommand(PaginationCommand):
    crm_user_id: int
    app_id: int


class GetAppPlatformCommand(FlexibleCommand):
    crm_user_id: int
    app_id: int
    platform_id: int


class CreateAppPlatformCommand(FlexibleCommand):
    crm_user_id: int
    app_id: int
    platform: str
    package_name: str
    install_key: str
    store_url: str | None = None
    status: str = "active"


class AppConfigurationCommand(FlexibleCommand):
    install_key: str
