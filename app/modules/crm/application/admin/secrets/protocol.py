from typing import Protocol

from app.modules.crm.application.admin.secrets.commands import (
    CreateAppSecretCommand,
    CreateSecretTemplateCommand,
    DeleteAppSecretCommand,
    DeleteSecretTemplateCommand,
    GetAppSecretValueCommand,
    GetSecretTemplatesCommand,
    ListAppSecretsCommand,
    ListSecretTemplatesCommand,
    UpdateAppSecretCommand,
    UpdateSecretTemplateCommand,
)
from app.modules.crm.application.admin.secrets.responses import (
    CreateAppSecretResponse,
    CreateSecretTemplateResponse,
    DeleteAppSecretResponse,
    DeleteSecretResponse,
    GetAppSecretResponse,
    GetSecretTemplatesResponse,
    ListAppSecretsResponse,
    ListSecretTemplatesResponse,
    UpdateAppSecretResponse,
    UpdateSecretTemplateResponse,
)


class SecretsServiceProtocol(Protocol):
    def get_secret_template(
        self,
        command: GetSecretTemplatesCommand,
    ) -> GetSecretTemplatesResponse: ...

    def list_secret_templates(
        self,
        command: ListSecretTemplatesCommand,
    ) -> ListSecretTemplatesResponse: ...

    def update_secret_template(
        self,
        command: UpdateSecretTemplateCommand,
    ) -> UpdateSecretTemplateResponse: ...

    def create_secret_template(
        self,
        command: CreateSecretTemplateCommand,
    ) -> CreateSecretTemplateResponse: ...

    def delete_secret(self, command: DeleteSecretTemplateCommand) -> DeleteSecretResponse: ...

    def create_app_secret(
        self,
        command: CreateAppSecretCommand,
    ) -> CreateAppSecretResponse: ...

    def get_app_secret(self, command: GetAppSecretValueCommand) -> GetAppSecretResponse: ...

    def list_app_secrets(
        self,
        command: ListAppSecretsCommand,
    ) -> ListAppSecretsResponse: ...

    def update_app_secret(
        self,
        command: UpdateAppSecretCommand,
    ) -> UpdateAppSecretResponse: ...

    def delete_app_secret(
        self,
        command: DeleteAppSecretCommand,
    ) -> DeleteAppSecretResponse: ...
