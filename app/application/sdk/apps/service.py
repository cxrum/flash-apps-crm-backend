from __future__ import annotations

from app.application.mapper import PaginationMapper
from app.application.sdk.apps.commands import CreateAppPlatformCommand, DeleteAppCommand, DeleteAppPlatformCommand, GetAppPlatformCommand, ListAppPlatformsCommand, AppConfigurationCommand, UpdateAppCommand, UpdateAppPlatformCommand
from app.application.contracts.encryption import EncryptionServiceProtocol
from app.application.sdk.apps.commands import CreateAppCommand, GetAppCommand, ListAppsCommand
from app.application.sdk.apps.exception import InvalidAppPlatform, SdkAppCreateFailed, SdkAppNotFound, SdkAppPlatformByInstallKeyNotFound, SdkAppPlatformCreateFailed, SdkAppPlatformRepositoryEmptyEntity
from app.application.sdk.apps.mappers import SdkAppResponsesMapper
from app.application.sdk.apps.responses import *
from app.domain.app.CrmAppEntity import CrmAppEntity
from app.domain.app_platform.CrmAppPlatformEntity import CrmAppPlatformEntity
from app.domain.app_secret.CrmAppSecretEntity import CrmAppSecretEntity
from app.domain.hash_protocol import HashProtocol
from app.domain.role.CrmRoleEntity import CrmRoleEntity
from app.domain.role.CrmRoleEntity import Roles
from app.domain.secret_template.CrmSecretTemplateEntity import CrmSecretTemplateEntity
from app.domain.uow import UnitOfWorkFactoryProtocol, UnitOfWorkProtocol
from app.domain.user_app_access import CrmUserAppAccessEntity
from app.domain.user_permissions.CrmUserPermissionEntity import CrmUserPermissionEntity


class AppService:
    def __init__(self, 
            uow_factory: UnitOfWorkFactoryProtocol, 
            encryption_service: EncryptionServiceProtocol,
            hash_service: HashProtocol
    ) -> None:
        self._uow_factory = uow_factory
        self._encryption_service = encryption_service
        self._hash_service = hash_service

    def _get_app(self, uow: UnitOfWorkProtocol, *, app_id: int) -> CrmAppEntity:
        saved_app = uow.app_repo.get_by_id(app_id)
        
        if saved_app is None or saved_app.app_id is None:
            raise SdkAppNotFound(app_id)
            
        return saved_app

    def _get_user_app_role(
        self,
        uow: UnitOfWorkProtocol,
        *,
        crm_user_id: int,
        app_id: int,
    ) -> CrmRoleEntity:
        app_access = uow.user_app_access_repo.get_by_user_and_app(crm_user_id, app_id)
        if app_access is None:
            raise PermissionError()

        role = uow.role_repo.get_by_id(app_access.role_id)
        if role is None:
            raise PermissionError()

        return role

    def get_app(self, command: GetAppCommand) -> GetAppResponse: 
        
        with self._uow_factory.create() as uow:
            saved_app = self._get_app(uow, app_id=command.app_id)
            
        return GetAppResponse(
            app=SdkAppResponsesMapper.app_domain_to_value(saved_app)
        )

    def get_apps(self, command: ListAppsCommand) -> AppListResponse:
        
        with self._uow_factory.create() as uow:
            app_access = uow.user_app_access_repo.list_by_user_id(
                command.crm_user_id,
                pagination=PaginationMapper.pagination_from_command(command)
            )
            apps = []
            for access in app_access:
                _app = uow.app_repo.get_by_id(access.app_id)
                
                if _app is None:
                    continue
                
                apps.append(_app)

        return AppListResponse(
            apps=[SdkAppResponsesMapper.app_domain_to_value(it) for it in apps]
        )

    def create_app(self, command: CreateAppCommand) -> CreateAppResponse:
        app = CrmAppEntity(
            name = command.name,
            code_slug = command.code_slug ,
            description = command.description,
            tech_description = command.tech_description,
            logo_url = command.logo_url,
            screenshots = command.screenshots,
        )
        
        with self._uow_factory.create() as uow:
            saved_app = uow.app_repo.save(app)
            
            if saved_app.app_id is None:
                raise SdkAppCreateFailed()
            
            admin_role = uow.role_repo.get_by_code(Roles.ADMIN)
            
            uow.user_app_access_repo.save(
                CrmUserAppAccessEntity.create(
                    user_id=command.crm_user_id,
                    app_id=saved_app.app_id,
                    role_id=admin_role.role_id
                )
            )
                        
        return CreateAppResponse(
            app=SdkAppResponsesMapper.app_domain_to_value(saved_app)
        )

    def update_app(self, command: UpdateAppCommand) -> UpdateAppResponse: 
    
        with self._uow_factory.create() as uow:
            saved_app = self._get_app(uow, app_id=command.app_id)
            
            saved_app.update(
                code=command.code,
                name=command.name,
                description = command.description,
                is_active = command.is_active
            )
            
            saved_app = uow.app_repo.save(saved_app)
            
        return UpdateAppResponse(
            app=SdkAppResponsesMapper.app_domain_to_value(saved_app)
        )
        
    def delete_app(self, command: DeleteAppCommand) -> DeleteAppResponse: 
        with self._uow_factory.create() as uow:
            saved_app = self._get_app(uow, app_id=command.app_id)
            saved_app = uow.app_repo.delete(command.app_id)
            
        return DeleteAppResponse(
            app=SdkAppResponsesMapper.app_domain_to_value(saved_app)
        )
    
    def get_app_platforms(self, command: ListAppPlatformsCommand) -> ListAppPlatformsResponse:

        with self._uow_factory.create() as uow:
            app = uow.app_repo.get_by_id(command.app_id)
            role = self._get_user_app_role(uow, crm_user_id=command.crm_user_id, app_id=command.app_id)
            
            if app is None:
                raise SdkAppNotFound(command.app_id)

            saved_platform_app = uow.app_platform_repo.list_by_app_id(command.app_id)
                
        return ListAppPlatformsResponse(
            app_platforms=[SdkAppResponsesMapper.app_platform_domain_to_value(it, sdk_secret_view=it.secret_view_for_role(role.code)) for it in saved_platform_app]
        )

    def create_app_platform(self, command: CreateAppPlatformCommand) -> CreatePlatformResponse:
        platform_app = CrmAppPlatformEntity.create(
            hasher=self._hash_service,
            app_id = command.app_id,
            platform = command.platform,
            package_name = command.package_name,
            install_key = command.install_key,
            store_url = command.store_url,
        )
        
        if not platform_app.is_valid_platform():
            raise InvalidAppPlatform(command.platform)

        with self._uow_factory.create() as uow:
            role = self._get_user_app_role(uow, crm_user_id=command.crm_user_id, app_id=command.app_id)
            app = uow.app_repo.get_by_id(platform_app.app_id)
            
            if app is None:
                raise SdkAppNotFound(platform_app.app_id)

            platform_app.encrypt_secret(self._encryption_service)
            saved_platform_app = uow.app_platform_repo.save(platform_app)
                
            if saved_platform_app.platform_id is None:
                raise SdkAppPlatformCreateFailed()

        secret_view = saved_platform_app.secret_view_for_role(role.code)
        
        return CreatePlatformResponse(
            app_platform=SdkAppResponsesMapper.app_platform_domain_to_value(
                saved_platform_app,
                sdk_secret_view=secret_view,
            ),
            sdk_secret=self._encryption_service.decrypt(secret_view),
        )

    def _get_app_platform(self, uow: UnitOfWorkProtocol, *, app_platform_id: int) -> CrmAppPlatformEntity:
        saved_platform_app = uow.app_platform_repo.get_by_id(app_platform_id)

        if saved_platform_app is None or saved_platform_app.platform_id is None:
            raise SdkAppPlatformRepositoryEmptyEntity()
        
        return saved_platform_app

    def get_app_platform(self, command: GetAppPlatformCommand) -> GetPlatformResponse:
        
        with self._uow_factory.create() as uow:
            saved_platform = self._get_app_platform(uow, app_platform_id=command.platform_id)
            role = self._get_user_app_role(uow, crm_user_id=command.crm_user_id, app_id=command.app_id)
            
        return GetPlatformResponse(
            app_platform=SdkAppResponsesMapper.app_platform_domain_to_value(
                saved_platform,
                sdk_secret_view=saved_platform.secret_view_for_role(role.code),
            )
        )
    
    def update_app_platform(self, command: UpdateAppPlatformCommand) -> UpdatePlatformResponse:
                
        with self._uow_factory.create() as uow:
            saved_platform = self._get_app_platform(uow, app_platform_id=command.platform_id)
            saved_platform.update(
                install_key=command.install_key,
                is_active=command.is_active,
            )
            saved_platform = uow.app_platform_repo.save(saved_platform)
            
        return UpdatePlatformResponse(
            app_platform=SdkAppResponsesMapper.app_platform_domain_to_value(saved_platform)
        )
    
    def delete_app_platform(self, command: DeleteAppPlatformCommand) -> DeletePlatformResponse:
        with self._uow_factory.create() as uow:
            saved_platform = self._get_app_platform(uow, app_platform_id=command.platform_id)
            saved_platform = uow.app_platform_repo.delete(command.app_id)
            
        return DeletePlatformResponse(
            app_platform=SdkAppResponsesMapper.app_platform_domain_to_value(saved_platform)
        )

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

    def get_app_config_secrets(self, command: AppConfigurationCommand) -> AppConfigQueryResponse:
        
        with self._uow_factory.create() as uow:
            app_platform = uow.app_platform_repo.get_by_install_key(command.install_key)
            
            if app_platform is None or app_platform.platform_id is None:
                raise SdkAppPlatformByInstallKeyNotFound(command.install_key)
            
            templates = uow.secret_template_repo.list_all()
            latest_secrets = self._latest_secrets_by_template(
                uow.app_secret_repo.list_active_by_app(
                    app_id=app_platform.app_id,
                    platform_id=app_platform.platform_id,
                )
            )

        configurations: list[AppConfigQueryEntry] = []
        for template in templates:
            if template.template_id is None:
                continue
            
            if template.is_server_private():
                continue
            
            secret = latest_secrets.get(template.template_id)
            
            if secret is None:
                continue
            
            value = self._encryption_service.decrypt(secret.encrypted_value)
            
            configurations.append(
                AppConfigQueryEntry(
                    code=template.code,
                    value=value,
                )
            )

        return AppConfigQueryResponse(platform_configurations=configurations)
