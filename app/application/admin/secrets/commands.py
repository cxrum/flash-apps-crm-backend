from datetime import datetime

from pydantic import Field

from app.application.base import FlexibleCommand, PaginationCommand


class GetSecretTemplatesCommand(FlexibleCommand):
    crm_user_id: int
    app_id: int
    template_id: int


class ListSecretTemplatesCommand(PaginationCommand):
    crm_user_id: int
    app_id: int

class CreateSecretTemplateCommand(FlexibleCommand):
    crm_user_id: int
    app_id: int
    code: str
    display_name: str
    secret_type: str
    scope: str
    is_masked: bool = True
    is_required: bool = False


class UpdateSecretTemplateCommand(FlexibleCommand):
    crm_user_id: int
    app_id: int
    template_id: int
    code: str | None = None
    display_name: str | None = None
    scope: str | None = None
    value_type: str | None = None
    is_masked: bool | None = None
    is_required: bool | None = None


class DeleteSecretTemplateCommand(FlexibleCommand):
    crm_user_id: int
    app_id: int
    template_id: int


class AppSecretValueCommand(FlexibleCommand):
    key: str
    value: str
    scope: str


class ListAppSecretsCommand(PaginationCommand):
    crm_user_id: int
    app_id: int
    platform_id: int | None = None


class CreateAppSecretCommand(FlexibleCommand):
    crm_user_id: int
    app_id: int
    secret_template_id: int
    value: str
    platform_id: int | None = None
    active_flag: bool = True
    version: float = 1


class GetAppSecretValueCommand(FlexibleCommand):
    crm_user_id: int
    app_id: int
    app_secret_id: int


class UpdateAppSecretCommand(FlexibleCommand):
    crm_user_id: int
    app_id: int
    secret_id: int
    value: str | None = None
    platform_id: int | None = None
    active_flag: bool | None = None
    version: float | None = None


class DeleteAppSecretCommand(FlexibleCommand):
    crm_user_id: int
    app_id: int
    secret_id: int


class UpsertAppSecretsCommand(FlexibleCommand):
    crm_user_id: int
    app_id: int
    platform_id: int | None = None
    secrets: list[AppSecretValueCommand] = Field(default_factory=list)