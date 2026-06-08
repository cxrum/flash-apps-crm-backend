
from dataclasses import dataclass, field
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.application.base import BaseResponse


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
    store_url: str | None = None
    sdk_public_key: str | None = None
    sdk_secret_encrypted: str | None = None
    status: str
    platform_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


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
        
class AppConfigQueryResponse(BaseResponse):
    platform_configurations: list[AppConfigQueryEntry]
