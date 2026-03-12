from app.application.contracts.encryption import EncryptionServiceProtocol
from app.application.sdk.entities import SdkApplicationConfigurationCommand, SdkCreateAppCommand, SdkCreateAppPlatformCommand
from app.application.exceptions import ApplicationLevelError
from app.application.sdk.mappers import SdkDomainMapper
from app.application.sdk.usecases.apps.responses import AppConfigQueryEntry, AppConfigQueryResponse, AppTemplateConfigQueryEntry, CreateAppResponse, CreatePlatformResponse
from app.domain.app_platform.CrmAppPlatformEntity import CrmAppPlatformEntity
from app.domain.app_secret.CrmAppSecretEntity import CrmAppSecretEntity
from app.domain.secret_template.CrmSecretTemplateEntity import CrmSecretTemplateEntity
from app.domain.uow import CrmUnitOfWorkProtocol


class AppService:
    def __init__(self, 
                 uow: CrmUnitOfWorkProtocol, 
                 encryption_service: EncryptionServiceProtocol
                 ) -> None:
        self._uow = uow
        self._encryption_service = encryption_service

    def create_app(self, command: SdkCreateAppCommand) -> CreateAppResponse:
        app = SdkDomainMapper.app_from_command(command)
        app.draft()

        saved_app = self._uow.app_repo.save(app)
            
        if saved_app.app_id is None:
            raise ApplicationLevelError("App repository returned entity without app_id")
        
        return CreateAppResponse(app_id=saved_app.app_id)

    def create_platform(self, command: SdkCreateAppPlatformCommand) -> CreatePlatformResponse:
        platform_app = SdkDomainMapper.app_platform_from_command(command)
        
        if not platform_app.is_valid_platform():
            raise ApplicationLevelError("App platform does not valid")

        app = self._uow.app_repo.get_by_id(platform_app.app_id)
        if app is None:
            raise ApplicationLevelError(f"App with id {platform_app.app_id} doesnt exist")

        saved_platform_app = self._uow.app_platform_repo.save(platform_app)
            
        if saved_platform_app.platform_id is None:
            raise ApplicationLevelError("App platfrom repository returned empty entity")
        
        return CreatePlatformResponse(platform_id=saved_platform_app.platform_id)

    @staticmethod
    def _select_platform(
        platforms: list[CrmAppPlatformEntity],
        platform: str,
    ) -> CrmAppPlatformEntity | None:
        for item in platforms:
            if item.platform == platform:
                return item
        return None

    @staticmethod
    def _latest_secrets_by_template(
        secrets: list[CrmAppSecretEntity],
    ) -> dict[int, CrmAppSecretEntity]:
        latest_by_template: dict[int, CrmAppSecretEntity] = {}
        for secret in secrets:
            current = latest_by_template.get(secret.template_id)
            if current is None or secret.version > current.version:
                latest_by_template[secret.template_id] = secret
        return latest_by_template

    @staticmethod
    def _build_template_entry(
        template: CrmSecretTemplateEntity,
        secret: CrmAppSecretEntity | None,
    ) -> AppTemplateConfigQueryEntry:
        return AppTemplateConfigQueryEntry(
            code=template.code,
            display_name=template.display_name,
            scope=template.scope,
            value_type=template.value_type,
            version=float(secret.version) if secret is not None else 1.0,
            is_masked=template.is_masked,
            is_required=template.is_required,
            is_active=secret.active_flag if secret is not None else False,
            created_at=secret.created_at if secret is not None else template.created_at,
            updated_at=secret.updated_at if secret is not None else template.updated_at,
        )

    def get_app_config_secrets(self, command: SdkApplicationConfigurationCommand) -> AppConfigQueryResponse:
        platform = self._select_platform(
            self._uow.app_platform_repo.list_by_app_id(command.app_id),
            command.platform,
        )
        
        if platform is None or platform.platform_id is None:
            raise ApplicationLevelError(
                f"Platform {command.platform} is not configured for app {command.app_id}",
            )

        templates = self._uow.secret_template_repo.list_all()
        latest_secrets = self._latest_secrets_by_template(
            self._uow.app_secret_repo.list_active_by_app(
                command.app_id,
                platform_id=platform.platform_id,
            )
        )

        configurations: list[AppConfigQueryEntry] = []
        for template in templates:
            if template.template_id is None:
                continue
            secret = latest_secrets.get(template.template_id)
            value = (
                self._encryption_service.decrypt(secret.encrypted_value)
                if secret is not None
                else None
            )
            configurations.append(
                AppConfigQueryEntry(
                    template=self._build_template_entry(template, secret),
                    value=value,
                )
            )

        return AppConfigQueryResponse(platform_configurations=configurations)
