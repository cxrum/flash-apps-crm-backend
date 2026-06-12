from dataclasses import field
from datetime import datetime

from app.application.base import BaseResponse, JsonDict


class AppResponseValue(BaseResponse):
    app_id: int
    name: str
    code_slug: str
    status: str
    description: str | None = None
    tech_description: str | None = None
    logo_url: str | None = None
    screenshots: list[str] = field(default_factory=list)
    created_at: datetime | None = None
    updated_at: datetime | None = None


class AppPlatformResponseValue(BaseResponse):
    app_id: int
    platform: str
    package_name: str
    install_key: str
    platform_id: int
    current_version: str
    store_url: str | None = None
    sdk_public_key: str | None = None
    sdk_secret_encrypted: str | None = None
    version_policy: JsonDict | None = None
    status: str
    created_at: datetime | None = None
    updated_at: datetime | None = None


class RotatePlatformSecretResponse(BaseResponse):
    new_sdk_secret: str


class CreateAppResponse(BaseResponse):
    app: AppResponseValue


class UpdateAppResponse(BaseResponse):
    app: AppResponseValue


class DeleteAppResponse(BaseResponse):
    app: AppResponseValue


class GetAppResponse(BaseResponse):
    app: AppResponseValue


class AppListResponse(BaseResponse):
    apps: list[AppResponseValue]


class ListAppPlatformsResponse(BaseResponse):
    app_platforms: list[AppPlatformResponseValue]


class CreatePlatformResponse(BaseResponse):
    app_platform: AppPlatformResponseValue
    sdk_secret: str


class UpdatePlatformResponse(BaseResponse):
    app_platform: AppPlatformResponseValue


class GetPlatformResponse(BaseResponse):
    app_platform: AppPlatformResponseValue


class DeletePlatformResponse(BaseResponse):
    app_platform: AppPlatformResponseValue


class AppConfigQueryEntry(BaseResponse):
    code: str
    value: str


class VersionControl(BaseResponse):
    required: bool = False
    current_version: str
    min_version: str | None = None
    max_version: str | None = None
    allowed_versions: list[str] | None = None
    blocked_versions: list[str] | None = None


class AppConfigQueryResponse(BaseResponse):
    version_control: VersionControl
    platform_configurations: list[AppConfigQueryEntry]
