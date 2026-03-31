from app.application.admin.crm_authorization.service import CrmAuthorizationService
from app.application.admin.secrets.commands import (
    DeleteAppSecretCommand,
    DeleteSecretTemplateCommand,
    UpdateAppSecretCommand,
)
from app.application.admin.secrets.commands import CreateAppSecretCommand, CreateSecretTemplateCommand, GetAppSecretValueCommand, GetSecretTemplatesCommand, ListAppSecretsCommand, ListSecretTemplatesCommand, UpdateSecretTemplateCommand
from app.application.admin.secrets.mappers import SecretsCommandsMapper, SecretsResponseMapper
from app.application.admin.secrets.responses import AppSecretResponseEntry, CreateAppSecretResponse, CreateSecretTemplateResponse, DeleteAppSecretResponse, DeleteSecretResponse, GetAppSecretResponse, GetSecretTemplatesResponse, ListAppSecretsResponse, ListSecretTemplatesResponse, UpdateAppSecretResponse, UpdateSecretTemplateResponse
from app.application.contracts.encryption import EncryptionServiceProtocol
from app.application.exceptions import ApplicationError
from app.application.mapper import PaginationMapper
from app.domain.app_secret.CrmAppSecretEntity import CrmAppSecretEntity
from app.domain.secret_template.CrmSecretTemplateEntity import CrmSecretTemplateEntity
from app.domain.uow import UnitOfWorkFactoryProtocol, UnitOfWorkProtocol

class SecretsService:
    def __init__(
        self,
        uow_factory: UnitOfWorkFactoryProtocol,
        authorization_service: CrmAuthorizationService,
        encryption_service: EncryptionServiceProtocol
    ) -> None:
        self._uow_factory = uow_factory
        self._authorization_service = authorization_service
        self._encryption_service = encryption_service

    @staticmethod
    def _require_crm_user_id(crm_user_id: int | None) -> int:
        if crm_user_id is None:
            raise ApplicationError("CRM user context is required")
        return crm_user_id
    
    def _check_admin_access(self, crm_user_id: int, app_id: int):
        has_admin_access = self._authorization_service.is_user_admin_permission_access(crm_user_id=crm_user_id, app_id=app_id)
        if not has_admin_access:
            raise ApplicationError()
        
    def _check_manager_access(self, crm_user_id: int, app_id: int):
        has_admin_access = self._authorization_service.is_user_manager_permission_access(crm_user_id=crm_user_id, app_id=app_id)
        if not has_admin_access:
            raise ApplicationError()
    
    @staticmethod
    def _get_secret_template(
        uow: UnitOfWorkProtocol,
        *,
        secret_template_id: int,
    ) -> CrmSecretTemplateEntity:
        template = uow.secret_template_repo.get_by_id(secret_template_id)
        if template is None:
            raise ApplicationError(f"")

        return template
    
    def get_secret_template(
        self,
        command: GetSecretTemplatesCommand
    ) -> GetSecretTemplatesResponse:
        self._authorization_service.check_user_app_access(crm_user_id=command.crm_user_id, app_id=command.app_id)
        self._check_manager_access(command.crm_user_id, command.app_id)

        with self._uow_factory.create() as uow:
            template = self._get_secret_template(uow, secret_template_id=command.template_id)
            
        return GetSecretTemplatesResponse(
            secret_templates=SecretsCommandsMapper.secret_template_domain_to_value(template)
        )
    
    def list_secret_templates(
        self,
        command: ListSecretTemplatesCommand,
    ) -> ListSecretTemplatesResponse:
        self._authorization_service.check_user_app_access(crm_user_id=command.crm_user_id, app_id=command.app_id)
        self._check_manager_access(command.crm_user_id, command.app_id)
        
        with self._uow_factory.create() as uow:
            
            # TODO Return templates that belong to the current user  
            templates = uow.secret_template_repo.list_all(
                pagination=PaginationMapper.pagination_from_command(command)
            )
            
        return ListSecretTemplatesResponse(
            secret_templates=[SecretsCommandsMapper.secret_template_domain_to_value(it) for it in templates]
        )

    def update_secret_template(
        self,
        command: UpdateSecretTemplateCommand,
    ) -> UpdateSecretTemplateResponse:
        self._authorization_service.check_user_app_access(crm_user_id=command.crm_user_id, app_id=command.app_id)
        crm_user_id = self._require_crm_user_id(command.crm_user_id)
        self._check_admin_access(crm_user_id, command.app_id)

        with self._uow_factory.create() as uow:
            existing_template = uow.secret_template_repo.get_by_id(command.template_id)
            
            if existing_template is None:
                raise ApplicationError("Secret template doesn't exist")

            existing_template.update(
                code=command.code,
                display_name=command.display_name,
                scope=command.scope,
                value_type=command.value_type,
                is_masked=command.is_masked,
                is_required=command.is_required,
            )
            
            saved_template = uow.secret_template_repo.save(existing_template)

        return UpdateSecretTemplateResponse(
            secret_template = SecretsCommandsMapper.secret_template_domain_to_value(saved_template)
        )

    def create_secret_template(
        self,
        command: CreateSecretTemplateCommand,
    ) -> CreateSecretTemplateResponse:
        self._authorization_service.check_user_app_access(crm_user_id=command.crm_user_id, app_id=command.app_id)
        self._check_admin_access(command.crm_user_id, command.app_id)
        
        entity = CrmSecretTemplateEntity(
            code = command.code,
            display_name = command.display_name,
            scope = command.scope,
            value_type = command.secret_type,
            is_masked = command.is_masked,
            is_required = command.is_required
        )

        with self._uow_factory.create() as uow:
            template = uow.secret_template_repo.save(entity)

        return CreateSecretTemplateResponse(
            secret_template = SecretsCommandsMapper.secret_template_domain_to_value(template)
        )
    
    def delete_secret(
        self, 
        command: DeleteSecretTemplateCommand
    ) -> DeleteSecretResponse:
        self._authorization_service.check_user_app_access(crm_user_id=command.crm_user_id, app_id=command.app_id)
        
        with self._uow_factory.create() as uow:
            app_secret = uow.secret_template_repo.delete(command.template_id)
        
        return DeleteSecretResponse(
            secret_templates=SecretsCommandsMapper.secret_template_domain_to_value(app_secret)
        )
    
    @staticmethod
    def _get_app_secret(
        uow: UnitOfWorkProtocol,
        *,
        secret_template_id: int,
        app_id: int,
        platform_id: int | None = None
    ) -> CrmAppSecretEntity:
        app_secret = uow.app_secret_repo.get_by_id(secret_template_id)
        
        if app_secret is None:
            raise ApplicationError("App secret doesn't exist")

        if platform_id is not None and app_secret.platform_id != platform_id:
            raise ApplicationError("App secret doesn't exist")

        if app_secret.platform_id is not None:
            platform = uow.app_platform_repo.get_by_id(app_secret.platform_id)
            if platform is None or platform.app_id != app_id:
                raise ApplicationError("App secret doesn't exist")
        elif platform_id is not None:
            raise ApplicationError("App secret doesn't exist")
        
        return app_secret
    
    def create_app_secret(
        self,
        command: CreateAppSecretCommand,
    ) -> CreateAppSecretResponse: 
        self._authorization_service.check_user_app_access(crm_user_id=command.crm_user_id, app_id=command.app_id)
        crm_user_id = self._require_crm_user_id(command.crm_user_id)
        
        encrypted_value=self._encryption_service.encrypt(command.value)
        
        entity = CrmAppSecretEntity(
                template_id = command.secret_template_id,
                encrypted_value = encrypted_value,
                platform_id = command.platform_id,
                active_flag = command.active_flag,
                version = command.version,
        )

        with self._uow_factory.create() as uow:
            secret = uow.app_secret_repo.save(entity)
            scoped_secrets = self._user_app_secrets_scope(
                uow,
                self._authorization_service,
                app_id=command.app_id,
                crm_user_id=crm_user_id,
                app_secrets=[secret],
                encryption_service=self._encryption_service,
            )
        
        return CreateAppSecretResponse(
            app_secret=scoped_secrets[0]
        ) 
    
    @staticmethod
    def _user_app_secrets_scope(
        uow: UnitOfWorkProtocol,
        user_service: CrmAuthorizationService,
        *,
        app_id: int,
        crm_user_id: int,
        app_secrets: list[CrmAppSecretEntity],
        encryption_service: EncryptionServiceProtocol
    ) -> list[AppSecretResponseEntry]:
        
        result_response: list[AppSecretResponseEntry] = []
        has_admin_access = user_service.is_user_admin_permission_access(crm_user_id=crm_user_id, app_id=app_id)
        
        for app_secret in app_secrets:
            template = uow.secret_template_repo.get_by_id(app_secret.template_id)
            
            if template is None or template.template_id is None:
                raise ApplicationError("Secret template doesn't exist")
            
            res_value = app_secret.encrypted_value
            
            if has_admin_access:
                decrypted_value = encryption_service.decrypt(app_secret.encrypted_value)
                res_value = decrypted_value
            else:
                if template.is_masked:
                    res_value = template.mask(res_value)
                
            result_response.append(
                AppSecretResponseEntry(
                    template_id=template.template_id,
                    secret_id=app_secret.secret_id,
                    display_name=template.display_name,
                    value=res_value,
                    platform_id=app_secret.platform_id,
                    active_flag=app_secret.active_flag,
                    version=app_secret.version,
                    created_at=app_secret.created_at,
                    updated_at=app_secret.updated_at,
                )
            )
        
        return result_response    
    
    def get_app_secret(
        self,
        command: GetAppSecretValueCommand,
    ) -> GetAppSecretResponse:
        self._authorization_service.check_user_app_access(crm_user_id=command.crm_user_id, app_id=command.app_id)
        crm_user_id = self._require_crm_user_id(command.crm_user_id)

        with self._uow_factory.create() as uow:
            app_secret = self._get_app_secret(
                uow,
                secret_template_id=command.app_secret_id,
                app_id=command.app_id,
            )
            scoped_secrets = self._user_app_secrets_scope(
                uow,
                self._authorization_service,
                app_id=command.app_id,
                crm_user_id=crm_user_id,
                app_secrets=[app_secret],
                encryption_service=self._encryption_service,
            )

        return GetAppSecretResponse(app_secret=scoped_secrets[0])
        
    def list_app_secrets(
        self,
        command: ListAppSecretsCommand,
    ) -> ListAppSecretsResponse:
        self._authorization_service.check_user_app_access(crm_user_id=command.crm_user_id, app_id=command.app_id)
        crm_user_id = self._require_crm_user_id(command.crm_user_id)

        with self._uow_factory.create() as uow:
            app_secrets = uow.app_secret_repo.list_by_app_id(
                command.app_id,
                platform_id=command.platform_id,
                pagination=PaginationMapper.pagination_from_command(command)
            )
            
            scoped_secrets = self._user_app_secrets_scope(
                uow,
                self._authorization_service,
                app_id=command.app_id,
                crm_user_id=crm_user_id,
                app_secrets=app_secrets,
                encryption_service=self._encryption_service,
            )

        return ListAppSecretsResponse(app_secrets=scoped_secrets)
    
    def update_app_secret(
        self,
        command: UpdateAppSecretCommand,
    ) -> UpdateAppSecretResponse:
        self._authorization_service.check_user_app_access(crm_user_id=command.crm_user_id, app_id=command.app_id)
        crm_user_id = self._require_crm_user_id(command.crm_user_id)
        self._check_admin_access(crm_user_id, command.app_id)

        has_admin_access = self._authorization_service.is_user_admin_permission_access(crm_user_id=crm_user_id, app_id=command.app_id)
        if not has_admin_access:
            raise ApplicationError()
        
        
        with self._uow_factory.create() as uow:
            app_secret = self._get_app_secret(
                uow,
                secret_template_id=command.secret_id,
                app_id=command.app_id,
            )

            platform_id = app_secret.platform_id
            if "platform_id" in command.model_fields_set:
                platform_id = command.platform_id

            encrypted_value = app_secret.encrypted_value
            if command.value is not None:
                encrypted_value = self._encryption_service.encrypt(command.value)

            active_flag = app_secret.active_flag if command.active_flag is None else command.active_flag
            version = app_secret.version if command.version is None else command.version

            updated_secret = CrmAppSecretEntity(
                template_id=app_secret.template_id,
                encrypted_value=encrypted_value,
                platform_id=platform_id,
                active_flag=active_flag,
                version=version,
                secret_id=app_secret.secret_id,
                created_at=app_secret.created_at,
            )
            saved_secret = uow.app_secret_repo.save(updated_secret)
            scoped_secrets = self._user_app_secrets_scope(
                uow,
                self._authorization_service,
                app_id=command.app_id,
                crm_user_id=crm_user_id,
                app_secrets=[saved_secret],
                encryption_service=self._encryption_service,
            )

        return UpdateAppSecretResponse(app_secret=scoped_secrets[0])
    
    def delete_app_secret(
        self, 
        command: DeleteAppSecretCommand 
    ) -> DeleteAppSecretResponse: 
        self._authorization_service.check_user_app_access(crm_user_id=command.crm_user_id, app_id=command.app_id)
        
        with self._uow_factory.create() as uow:
            app_secret = uow.app_secret_repo.delete(command.secret_id)
        
        return DeleteAppSecretResponse(
            app_secret=SecretsCommandsMapper.app_secret_domain_to_value(app_secret)
        )
    
        