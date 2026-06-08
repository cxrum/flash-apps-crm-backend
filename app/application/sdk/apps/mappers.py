from collections.abc import Mapping
from dataclasses import asdict

from app.application.sdk.apps.commands import CreateAppCommand, CreateAppPlatformCommand, DeleteAppCommand, DeleteAppPlatformCommand, GetAppCommand, GetAppPlatformCommand, ListAppPlatformsCommand, ListAppsCommand, UpdateAppCommand, UpdateAppPlatformCommand
from app.application.sdk.apps.responses import AppPlatformResponseValue, AppResponseValue
from app.core.utils.general_mapper import GeneralMapper
from app.domain.app.CrmAppEntity import CrmAppEntity
from app.domain.app_platform import CrmAppPlatformEntity

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
        response = AppPlatformResponseValue.model_validate(domain)
        return response.model_copy(update={"sdk_secret_encrypted": sdk_secret_view})
    
    
