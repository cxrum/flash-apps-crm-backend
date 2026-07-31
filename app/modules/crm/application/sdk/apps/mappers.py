from collections.abc import Mapping
from dataclasses import asdict

from app.core.utils.general_mapper import GeneralMapper
from app.modules.crm.application.sdk.apps.commands import (
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
from app.modules.crm.application.sdk.apps.responses import AppPlatformResponseValue, AppResponseValue
from app.modules.crm.domain.app.CrmAppEntity import CrmAppEntity
from app.modules.crm.domain.app_platform import CrmAppPlatformEntity


class SdkAppCommandsMapper:
    @classmethod
    def list_apps_from_transport(cls, payload: Mapping[str, object]) -> ListAppsCommand:
        return GeneralMapper.command_payload_to_command(ListAppsCommand, payload)

    @classmethod
    def create_app_from_transport(cls, payload: Mapping[str, object]) -> CreateAppCommand:
        return GeneralMapper.command_payload_to_command(CreateAppCommand, payload)

    @classmethod
    def get_app_from_transport(cls, payload: Mapping[str, object]) -> GetAppCommand:
        return GeneralMapper.command_payload_to_command(GetAppCommand, payload)

    @classmethod
    def update_app_from_transport(cls, payload: Mapping[str, object]) -> UpdateAppCommand:
        return GeneralMapper.command_payload_to_command(UpdateAppCommand, payload)

    @classmethod
    def delete_app_from_transport(cls, payload: Mapping[str, object]) -> DeleteAppCommand:
        return GeneralMapper.command_payload_to_command(DeleteAppCommand, payload)

    @classmethod
    def list_app_platforms_from_transport(cls, payload: Mapping[str, object]) -> ListAppPlatformsCommand:
        return GeneralMapper.command_payload_to_command(ListAppPlatformsCommand, payload)

    @classmethod
    def get_app_platform_from_transport(cls, payload: Mapping[str, object]) -> GetAppPlatformCommand:
        return GeneralMapper.command_payload_to_command(GetAppPlatformCommand, payload)

    @classmethod
    def create_app_platform_from_transport(cls, payload: Mapping[str, object]) -> CreateAppPlatformCommand:
        return GeneralMapper.command_payload_to_command(CreateAppPlatformCommand, payload)

    @classmethod
    def update_app_platform_from_transport(cls, payload: Mapping[str, object]) -> UpdateAppPlatformCommand:
        return GeneralMapper.command_payload_to_command(UpdateAppPlatformCommand, payload)

    @classmethod
    def delete_app_platform_from_transport(cls, payload: Mapping[str, object]) -> DeleteAppPlatformCommand:
        return GeneralMapper.command_payload_to_command(DeleteAppPlatformCommand, payload)

    @classmethod
    def rotate_platform_secret_from_transport(cls, payload: Mapping[str, object]) -> RotatePlatformSecretCommand:
        return GeneralMapper.command_payload_to_command(RotatePlatformSecretCommand, payload)


class SdkAppResponsesMapper:
    @classmethod
    def app_domain_to_value(cls, domain: CrmAppEntity) -> AppResponseValue:
        return AppResponseValue.model_validate(domain)

    @classmethod
    def app_platform_domain_to_value(
        cls,
        domain: CrmAppPlatformEntity,
        *,
        sdk_secret_view: str | None = None,
    ) -> AppPlatformResponseValue:
        payload = dict(vars(domain))
        payload.pop("_sdk_secret_plain", None)
        payload["version_policy"] = domain.version_policy_dict()
        payload["sdk_secret_encrypted"] = sdk_secret_view
        return AppPlatformResponseValue.model_validate(payload)
