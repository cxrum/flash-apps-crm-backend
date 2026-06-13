from typing import Mapping

from app.modules.crm.application.admin.secrets.commands import (
    CreateSecretTemplateCommand,
    DeleteAppSecretCommand,
    DeleteSecretTemplateCommand,
    GetAppSecretValueCommand,
    GetSecretTemplatesCommand,
    ListAppSecretsCommand,
    ListSecretTemplatesCommand,
    UpdateAppSecretCommand,
    UpdateSecretTemplateCommand,
    UpsertAppSecretsCommand,
)
from app.modules.crm.application.admin.secrets.responses import AppSecretResponseEntry, SecretTemplateResponseEntry
from app.modules.crm.core.utils.general_mapper import GeneralMapper
from app.modules.crm.domain.app_secret.CrmAppSecretEntity import CrmAppSecretEntity
from app.modules.crm.domain.secret_template.CrmSecretTemplateEntity import CrmSecretTemplateEntity


class SecretsResponseMapper:
    @classmethod
    def list_secret_templates_from_transport(cls, payload: Mapping[str, object]) -> ListSecretTemplatesCommand:
        return GeneralMapper.command_payload_to_command(ListSecretTemplatesCommand, payload)

    @classmethod
    def get_secret_template_from_transport(cls, payload: Mapping[str, object]) -> GetSecretTemplatesCommand:
        return GeneralMapper.command_payload_to_command(GetSecretTemplatesCommand, payload)

    @classmethod
    def create_secret_template_from_transport(cls, payload: Mapping[str, object]) -> CreateSecretTemplateCommand:
        return GeneralMapper.command_payload_to_command(CreateSecretTemplateCommand, payload)

    @classmethod
    def update_secret_template_from_transport(cls, payload: Mapping[str, object]) -> UpdateSecretTemplateCommand:
        return GeneralMapper.command_payload_to_command(UpdateSecretTemplateCommand, payload)

    @classmethod
    def delete_secret_template_from_transport(
        cls,
        payload: Mapping[str, object],
    ) -> DeleteSecretTemplateCommand:
        return GeneralMapper.command_payload_to_command(DeleteSecretTemplateCommand, payload)

    @classmethod
    def list_app_secrets_from_transport(cls, payload: Mapping[str, object]) -> ListAppSecretsCommand:
        return GeneralMapper.command_payload_to_command(ListAppSecretsCommand, payload)

    @classmethod
    def get_app_secret_from_transport(cls, payload: Mapping[str, object]) -> GetAppSecretValueCommand:
        return GeneralMapper.command_payload_to_command(GetAppSecretValueCommand, payload)

    @classmethod
    def update_app_secret_from_transport(cls, payload: Mapping[str, object]) -> UpdateAppSecretCommand:
        return GeneralMapper.command_payload_to_command(UpdateAppSecretCommand, payload)

    @classmethod
    def delete_app_secret_from_transport(cls, payload: Mapping[str, object]) -> DeleteAppSecretCommand:
        return GeneralMapper.command_payload_to_command(DeleteAppSecretCommand, payload)

    @classmethod
    def upsert_app_secrets_from_transport(cls, payload: Mapping[str, object]) -> UpsertAppSecretsCommand:
        return GeneralMapper.command_payload_to_command(UpsertAppSecretsCommand, payload)


class SecretsCommandsMapper:
    @classmethod
    def app_secret_domain_to_value(cls, domain: CrmAppSecretEntity) -> AppSecretResponseEntry:
        return AppSecretResponseEntry.model_validate(domain)

    @classmethod
    def secret_template_domain_to_value(cls, domain: CrmSecretTemplateEntity) -> SecretTemplateResponseEntry:
        return SecretTemplateResponseEntry.model_validate(domain)
