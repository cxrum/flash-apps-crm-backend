from dataclasses import dataclass
from datetime import datetime

from app.application.base import BaseResponse


class AppSecretResponseEntry(BaseResponse):
    template_id: int
    display_name: str
    value: str
    platform_id: int | None = None
    active_flag: bool = True
    version: float = 1
    secret_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class CreateAppSecretResponse(BaseResponse):
    app_secret: AppSecretResponseEntry


class UpdateAppSecretResponse(BaseResponse):
    app_secret: AppSecretResponseEntry


class ListAppSecretsResponse(BaseResponse):
    app_secrets: list[AppSecretResponseEntry]


class GetAppSecretResponse(BaseResponse):
    app_secret: AppSecretResponseEntry

class DeleteAppSecretResponse(BaseResponse):
    app_secret: AppSecretResponseEntry

class SecretTemplateResponseEntry(BaseResponse):
    code: str
    display_name: str
    scope: str
    value_type: str
    is_masked: bool = True
    is_required: bool = False
    template_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class CreateSecretTemplateResponse(BaseResponse):
    secret_template: SecretTemplateResponseEntry

class UpdateSecretTemplateResponse(BaseResponse):
    secret_template: SecretTemplateResponseEntry

class ListSecretTemplatesResponse(BaseResponse):
    secret_templates: list[SecretTemplateResponseEntry]

class GetSecretTemplatesResponse(BaseResponse):
    secret_templates: SecretTemplateResponseEntry
    
class DeleteSecretResponse(BaseResponse):
    secret_templates: SecretTemplateResponseEntry