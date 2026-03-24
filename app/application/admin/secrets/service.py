from app.application.admin.crm_users.service import CrmUsersService
from app.application.admin.entities import (
    CreateAppSecretCommand,
    CreateSecretTemplateCommand,
    GetAppSecretValueCommand,
    GetSecretTemplatesCommand,
    ListAppSecretsCommand,
    ListSecretTemplatesCommand,
    UpdateAppSecretCommand,
    UpdateSecretTemplateCommand,
)
from app.application.admin.responses import (
    AppSecretResponseEntry,
    CreateAppSecretResponse,
    CreateSecretTemplateResponse,
    GetAppSecretResponse,
    GetSecretTemplatesResponse,
    ListAppSecretsResponse,
    ListSecretTemplatesResponse,
    UpdateAppSecretResponse,
)
from app.application.contracts.encryption import EncryptionServiceProtocol
from app.application.exceptions import ApplicationError
from app.domain.app_secret.CrmAppSecretEntity import CrmAppSecretEntity
from app.domain.secret_template.CrmSecretTemplateEntity import CrmSecretTemplateEntity
from app.domain.uow import UnitOfWorkFactoryProtocol, UnitOfWorkProtocol
from app.application.admin.mappers import AdminDomainMapper, AdminResponseMapper


class SecretsService:
    def __init__(
        self,
        uow_factory: UnitOfWorkFactoryProtocol,
        user_service: CrmUsersService,
        encryption_service: EncryptionServiceProtocol
    ) -> None:
        self._uow_factory = uow_factory
        self._user_service = user_service
        self._encryption_service = encryption_service

    @staticmethod
    def _require_crm_user_id(crm_user_id: int | None) -> int:
        if crm_user_id is None:
            raise ApplicationError("CRM user context is required")
        return crm_user_id
    
    def _check_admin_access(self, crm_user_id: int, app_id: int):
        has_admin_access = self._user_service.is_user_admin_permision_access(crm_user_id=crm_user_id, app_id=app_id)
        if not has_admin_access:
            raise ApplicationError()
        
    def _check_manager_access(self, crm_user_id: int, app_id: int):
        has_admin_access = self._user_service.is_user_manager_permision_access(crm_user_id=crm_user_id, app_id=app_id)
        if not has_admin_access:
            raise ApplicationError()
    
    @staticmethod
    def _get_secret_tempalte(
        uow: UnitOfWorkProtocol,
        *,
        secret_tempalte_id: int,
    ) -> CrmSecretTemplateEntity:
        tempalte = uow.secret_template_repo.get_by_id(secret_tempalte_id)
        if tempalte is None:
            raise ApplicationError(f"")

        return tempalte
    
    def get_secret_tempalte(
        self,
        command: GetSecretTemplatesCommand
    ) -> GetSecretTemplatesResponse:
        self._user_service.check_user_app_access(crm_user_id=command.crm_user_id, app_id=command.app_id)
        self._check_manager_access(command.crm_user_id, command.app_id)

        with self._uow_factory.create() as uow:
            template = self._get_secret_tempalte(uow, secret_tempalte_id=command.template_id)
            
        return GetSecretTemplatesResponse(
            secret_templates=AdminResponseMapper.secret_template_from_domain(template)
        )
    
    def list_secret_templates(
        self,
        command: ListSecretTemplatesCommand,
    ) -> ListSecretTemplatesResponse:
        self._user_service.check_user_app_access(crm_user_id=command.crm_user_id, app_id=command.app_id)
        self._check_manager_access(command.crm_user_id, command.app_id)
        
        with self._uow_factory.create() as uow:
            templates = uow.secret_template_repo.list_all()
            
        return AdminResponseMapper.list_secret_templates_from_domain(templates)


    def update_secret_template(
        self,
        command: UpdateSecretTemplateCommand,
    ) -> CreateSecretTemplateResponse:
        self._user_service.check_user_app_access(crm_user_id=command.crm_user_id, app_id=command.app_id)
        crm_user_id = self._require_crm_user_id(command.crm_user_id)
        self._check_admin_access(crm_user_id, command.app_id)

        mapped_template = AdminDomainMapper.secret_template_from_update_command(command)

        if mapped_template.template_id is None:
            raise ApplicationError()
        
        with self._uow_factory.create() as uow:
            existing_template = uow.secret_template_repo.get_by_id(mapped_template.template_id)
            
            if existing_template is None:
                raise ApplicationError("Secret template doesnt exist")

            updated_template = CrmSecretTemplateEntity(
                code=existing_template.code,
                display_name=mapped_template.display_name,
                scope=mapped_template.scope,
                value_type=mapped_template.value_type,
                is_masked=existing_template.is_masked,
                is_required=existing_template.is_required,
                template_id=existing_template.template_id,
                created_at=existing_template.created_at,
            )
            saved_template = uow.secret_template_repo.save(updated_template)

        return AdminResponseMapper.create_secret_template_from_domain(saved_template)

    def create_secret_template(
        self,
        command: CreateSecretTemplateCommand,
    ) -> CreateSecretTemplateResponse:
        self._user_service.check_user_app_access(crm_user_id=command.crm_user_id, app_id=command.app_id)
        self._check_admin_access(command.crm_user_id, command.app_id)
        
        entity = AdminDomainMapper.secret_template_from_command(command)

        with self._uow_factory.create() as uow:
            template = uow.secret_template_repo.save(entity)

        return AdminResponseMapper.create_secret_template_from_domain(template)
        
    
    @staticmethod
    def _get_app_secret(
        uow: UnitOfWorkProtocol,
        *,
        secret_tempalte_id: int,
        app_id: int,
        platform_id: int | None = None
    ) -> CrmAppSecretEntity:
        app_secret = uow.app_secret_repo.get_by_id(secret_tempalte_id)
        if app_secret is None:
            raise ApplicationError("App secret doesnt exist")

        if platform_id is not None and app_secret.platform_id != platform_id:
            raise ApplicationError("App secret doesnt exist")

        if app_secret.platform_id is not None:
            platform = uow.app_platform_repo.get_by_id(app_secret.platform_id)
            if platform is None or platform.app_id != app_id:
                raise ApplicationError("App secret doesnt exist")
        elif platform_id is not None:
            raise ApplicationError("App secret doesnt exist")
        
        return app_secret
    
    
    def create_app_secret(
        self,
        command: CreateAppSecretCommand,
    ) -> CreateAppSecretResponse: 
        self._user_service.check_user_app_access(crm_user_id=command.crm_user_id, app_id=command.app_id)
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
                self._user_service,
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
        user_service: CrmUsersService,
        *,
        app_id: int,
        crm_user_id: int,
        app_secrets: list[CrmAppSecretEntity],
        encryption_service: EncryptionServiceProtocol
    ) -> list[AppSecretResponseEntry]:
        
        result_response: list[AppSecretResponseEntry] = []
        has_admin_access = user_service.is_user_admin_permision_access(crm_user_id=crm_user_id, app_id=app_id)
        
        for app_secret in app_secrets:
            template = uow.secret_template_repo.get_by_id(app_secret.template_id)
            
            if template is None or template.template_id is None:
                raise ApplicationError("Secret template doesnt exist")
            
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
        self._user_service.check_user_app_access(crm_user_id=command.crm_user_id, app_id=command.app_id)
        crm_user_id = self._require_crm_user_id(command.crm_user_id)

        with self._uow_factory.create() as uow:
            app_secret = self._get_app_secret(
                uow,
                secret_tempalte_id=command.app_secret_id,
                app_id=command.app_id,
            )
            scoped_secrets = self._user_app_secrets_scope(
                uow,
                self._user_service,
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
        self._user_service.check_user_app_access(crm_user_id=command.crm_user_id, app_id=command.app_id)
        crm_user_id = self._require_crm_user_id(command.crm_user_id)

        with self._uow_factory.create() as uow:
            app_secrets = uow.app_secret_repo.list_by_app_id(
                command.app_id,
                platform_id=command.platform_id,
            )
            scoped_secrets = self._user_app_secrets_scope(
                uow,
                self._user_service,
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
        self._user_service.check_user_app_access(crm_user_id=command.crm_user_id, app_id=command.app_id)
        crm_user_id = self._require_crm_user_id(command.crm_user_id)
        self._check_admin_access(crm_user_id, command.app_id)

        has_admin_access = self._user_service.is_user_admin_permision_access(crm_user_id=crm_user_id, app_id=command.app_id)
        if not has_admin_access:
            raise ApplicationError()
        
        
        with self._uow_factory.create() as uow:
            app_secret = self._get_app_secret(
                uow,
                secret_tempalte_id=command.secret_id,
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
                self._user_service,
                app_id=command.app_id,
                crm_user_id=crm_user_id,
                app_secrets=[saved_secret],
                encryption_service=self._encryption_service,
            )

        return UpdateAppSecretResponse(app_secret=scoped_secrets[0])
    
    
