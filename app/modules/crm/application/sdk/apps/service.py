from __future__ import annotations

from app.modules.crm.application.access_decorators import require_app_access, require_role
from app.modules.crm.application.admin.crm_authorization.protocol import CrmAuthorizationServiceProtocol
from app.modules.crm.application.contracts.encryption import EncryptionServiceProtocol
from app.modules.crm.application.exception import RoleNotFound
from app.modules.crm.application.mapper import PaginationMapper
from app.modules.crm.application.sdk.apps.commands import (
    AppConfigurationCommand,
    CreateAppCommand,
    CreateAppPlatformCommand,
    DeleteAppCommand,
    DeleteAppPlatformCommand,
    GetAppCommand,
    GetAppPlatformCommand,
    ListAppPlatformsCommand,
    ListAppsCommand,
    RotatePlatformSecretCommand,
    UpdateAppCommand,
    UpdateAppPlatformCommand,
)
from app.modules.crm.application.sdk.apps.exception import (
    InvalidAppPlatform,
    SdkAppCreateFailed,
    SdkAppNotFound,
    SdkAppPlatformByInstallKeyNotFound,
    SdkAppPlatformCreateFailed,
    SdkAppPlatformRepositoryEmptyEntity,
)
from app.modules.crm.application.sdk.apps.mappers import SdkAppResponsesMapper
from app.modules.crm.application.sdk.apps.protocol import AppServiceProtocol
from app.modules.crm.application.sdk.apps.responses import (
    AppConfigQueryEntry,
    AppConfigQueryResponse,
    AppListResponse,
    CreateAppResponse,
    CreatePlatformResponse,
    DeleteAppResponse,
    DeletePlatformResponse,
    GetAppResponse,
    GetPlatformResponse,
    ListAppPlatformsResponse,
    RotatePlatformSecretResponse,
    UpdateAppResponse,
    UpdatePlatformResponse,
    VersionControl,
)
from app.modules.crm.domain.app.CrmAppEntity import CrmAppEntity
from app.modules.crm.domain.app_platform.CrmAppPlatformEntity import CrmAppPlatformEntity
from app.modules.crm.domain.app_secret.CrmAppSecretEntity import CrmAppSecretEntity
from app.modules.crm.domain.hash_protocol import HashProtocol
from app.modules.crm.domain.role.CrmRoleEntity import CrmRoleEntity, Roles
from app.modules.crm.domain.uow import UnitOfWorkFactoryProtocol, UnitOfWorkProtocol
from app.modules.crm.domain.user_app_access.CrmUserAppAccessEntity import CrmUserAppAccessEntity


class AppService(AppServiceProtocol):
    def __init__(
        self,
        uow_factory: UnitOfWorkFactoryProtocol,
        authorization_service: CrmAuthorizationServiceProtocol,
        encryption_service: EncryptionServiceProtocol,
        hash_service: HashProtocol,
    ) -> None:
        self._uow_factory = uow_factory
        self._authorization_service = authorization_service
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
        return self._authorization_service.get_user_role(
            uow=uow,
            crm_user_id=crm_user_id,
            app_id=app_id,
        )

    @staticmethod
    def _platform_response_with_secret(
        platform: CrmAppPlatformEntity,
        role: CrmRoleEntity,
    ):
        secret_view = platform.secret_view_for_role(role.code)
        return SdkAppResponsesMapper.app_platform_domain_to_value(
            platform,
            sdk_secret_view=secret_view,
        ), secret_view

    @require_app_access()
    def get_app(self, command: GetAppCommand) -> GetAppResponse:
        with self._uow_factory.create() as uow:
            saved_app = self._get_app(uow, app_id=command.app_id)

        return GetAppResponse(app=SdkAppResponsesMapper.app_domain_to_value(saved_app))

    def get_apps(self, command: ListAppsCommand) -> AppListResponse:
        with self._uow_factory.create() as uow:
            app_access = uow.user_app_access_repo.list_by_user_id(
                command.crm_user_id,
                pagination=PaginationMapper.pagination_from_command(command),
            )
            apps = []
            for access in app_access:
                app = uow.app_repo.get_by_id(access.app_id)

                if app is None:
                    continue

                apps.append(app)

        return AppListResponse(apps=[SdkAppResponsesMapper.app_domain_to_value(it) for it in apps])

    def _rotate_platform_secret(
        self, uow: UnitOfWorkProtocol, *, command: RotatePlatformSecretCommand
    ) -> CrmAppPlatformEntity:
        saved_app = uow.app_repo.get_by_id(command.app_id)

        if saved_app is None or saved_app.app_id is None:
            raise SdkAppNotFound(command.app_id)

        saved_platform = uow.app_platform_repo.get_by_id(command.platform_id)

        if saved_platform is None or saved_platform.app_id is None:
            raise SdkAppPlatformRepositoryEmptyEntity()

        saved_platform.rotate_secret(
            hasher=self._hash_service,
            encryption=self._encryption_service,
        )
        saved_platform = uow.app_platform_repo.save(saved_platform)

        return saved_platform

    @require_role(Roles.ADMIN)
    def rotate_platform_secret(self, command: RotatePlatformSecretCommand) -> RotatePlatformSecretResponse:
        with self._uow_factory.create() as uow:
            saved = self._rotate_platform_secret(uow, command=command)

            if saved.sdk_secret_fallback_encrypted is None:
                raise SdkAppPlatformRepositoryEmptyEntity()

        return RotatePlatformSecretResponse(
            new_sdk_secret=self._encryption_service.decrypt(saved.sdk_secret_fallback_encrypted)
        )

    def create_app(self, command: CreateAppCommand) -> CreateAppResponse:
        app = CrmAppEntity.create(
            name=command.name,
            code_slug=command.code_slug,
            description=command.description,
            tech_description=command.tech_description,
            logo_url=command.logo_url,
            screenshots=command.screenshots,
            status=command.status,
        )

        with self._uow_factory.create() as uow:
            saved_app = uow.app_repo.save(app)

            if saved_app.app_id is None:
                raise SdkAppCreateFailed()

            admin_role = uow.role_repo.get_by_code(Roles.ADMIN)

            if admin_role is None or admin_role.role_id is None:
                raise RoleNotFound()

            uow.user_app_access_repo.save(
                CrmUserAppAccessEntity.create(
                    user_id=command.crm_user_id,
                    app_id=saved_app.app_id,
                    role_id=admin_role.role_id,
                )
            )

        return CreateAppResponse(app=SdkAppResponsesMapper.app_domain_to_value(saved_app))

    @require_role(Roles.MANAGER)
    def update_app(self, command: UpdateAppCommand) -> UpdateAppResponse:
        with self._uow_factory.create() as uow:
            saved_app = self._get_app(uow, app_id=command.app_id)
            saved_app.update(
                code_slug=command.code, name=command.name, description=command.description, status=command.status
            )
            saved_app = uow.app_repo.save(saved_app)

        return UpdateAppResponse(app=SdkAppResponsesMapper.app_domain_to_value(saved_app))

    @require_role(Roles.MANAGER)
    def delete_app(self, command: DeleteAppCommand) -> DeleteAppResponse:
        with self._uow_factory.create() as uow:
            saved_app = self._get_app(uow, app_id=command.app_id)
            saved_app = uow.app_repo.delete(command.app_id)

        return DeleteAppResponse(app=SdkAppResponsesMapper.app_domain_to_value(saved_app))

    @require_app_access()
    def get_app_platforms(self, command: ListAppPlatformsCommand) -> ListAppPlatformsResponse:
        with self._uow_factory.create() as uow:
            app = uow.app_repo.get_by_id(command.app_id)
            role = self._get_user_app_role(uow, crm_user_id=command.crm_user_id, app_id=command.app_id)

            if app is None:
                raise SdkAppNotFound(command.app_id)

            saved_platform_app = uow.app_platform_repo.list_by_app_id(command.app_id)
            response_platforms = [
                self._platform_response_with_secret(platform, role)[0] for platform in saved_platform_app
            ]

        return ListAppPlatformsResponse(app_platforms=response_platforms)

    @require_role(Roles.ADMIN)
    def create_app_platform(self, command: CreateAppPlatformCommand) -> CreatePlatformResponse:
        platform_app = CrmAppPlatformEntity.create(
            hasher=self._hash_service,
            app_id=command.app_id,
            platform=command.platform,
            package_name=command.package_name,
            install_key=command.install_key,
            store_url=command.store_url,
            current_version=command.current_version,
            version_policy=command.version_policy,
            status=command.status,
        )

        if not platform_app.is_valid_platform():
            raise InvalidAppPlatform(command.platform)

        with self._uow_factory.create() as uow:
            role = self._get_user_app_role(uow, crm_user_id=command.crm_user_id, app_id=command.app_id)
            app = uow.app_repo.get_by_id(platform_app.app_id)

            if app is None or app.app_id is None:
                raise SdkAppNotFound(platform_app.app_id)

            platforms = uow.app_platform_repo.list_by_app_id(app.app_id)
            platform_app.uniq_per_app(platforms)

            platform_app.encrypt_secret(self._encryption_service)
            saved_platform_app = uow.app_platform_repo.save(platform_app)

            if saved_platform_app.platform_id is None:
                raise SdkAppPlatformCreateFailed()

            app_platform_response, secret_view = self._platform_response_with_secret(saved_platform_app, role)

        return CreatePlatformResponse(
            app_platform=app_platform_response,
            sdk_secret=self._encryption_service.decrypt(secret_view),
        )

    def _get_app_platform(self, uow: UnitOfWorkProtocol, *, app_platform_id: int) -> CrmAppPlatformEntity:
        saved_platform_app = uow.app_platform_repo.get_by_id(app_platform_id)

        if saved_platform_app is None or saved_platform_app.platform_id is None:
            raise SdkAppPlatformRepositoryEmptyEntity()

        return saved_platform_app

    @require_app_access()
    def get_app_platform(self, command: GetAppPlatformCommand) -> GetPlatformResponse:
        with self._uow_factory.create() as uow:
            saved_platform = self._get_app_platform(uow, app_platform_id=command.platform_id)
            role = self._get_user_app_role(uow, crm_user_id=command.crm_user_id, app_id=command.app_id)
            app_platform_response, _ = self._platform_response_with_secret(saved_platform, role)

        return GetPlatformResponse(app_platform=app_platform_response)

    @require_role(Roles.MANAGER)
    def update_app_platform(self, command: UpdateAppPlatformCommand) -> UpdatePlatformResponse:
        with self._uow_factory.create() as uow:
            saved_platform = self._get_app_platform(uow, app_platform_id=command.platform_id)

            saved_platform.update(
                install_key=command.install_key,
                package_name=command.package_name,
                store_url=command.store_url,
                current_version=command.current_version,
                version_policy=command.version_policy,
                status=command.status,
            )
            saved_platform = uow.app_platform_repo.save(saved_platform)

        return UpdatePlatformResponse(app_platform=SdkAppResponsesMapper.app_platform_domain_to_value(saved_platform))

    @require_role(Roles.ADMIN)
    def delete_app_platform(self, command: DeleteAppPlatformCommand) -> DeletePlatformResponse:
        with self._uow_factory.create() as uow:
            saved_platform = self._get_app_platform(uow, app_platform_id=command.platform_id)
            saved_platform = uow.app_platform_repo.delete(command.platform_id)

        return DeletePlatformResponse(app_platform=SdkAppResponsesMapper.app_platform_domain_to_value(saved_platform))

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

        if app_platform.version_policy:
            version_control_res = (
                VersionControl(
                    required=app_platform.version_policy.required,
                    current_version=app_platform.current_version,
                    min_version=app_platform.version_policy.min_version,
                    max_version=app_platform.version_policy.max_version,
                    allowed_versions=app_platform.version_policy.allowed_versions,
                    blocked_versions=app_platform.version_policy.blocked_versions,
                ),
            )

        else:
            version_control_res = (
                VersionControl(
                    required=False,
                    current_version=app_platform.current_version,
                    min_version=None,
                    max_version=None,
                    allowed_versions=None,
                    blocked_versions=None,
                ),
            )

        return AppConfigQueryResponse(
            version_control=version_control_res[0],
            platform_configurations=configurations,
        )
