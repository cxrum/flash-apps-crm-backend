from __future__ import annotations

from collections.abc import Mapping
from typing import TypeVar

from pydantic import BaseModel

from app.application.sdk.entities import (
    GetSdkConfigCommand,
    SdkCreateAppCommand,
    SdkCreateAppPlatformCommand,
    SdkEventsCommand,
    SdkInstallCommand,
    SdkParamsUpdateCommand,
    SdkPushRegisterCommand,
)
from app.domain.app.CrmAppEntity import CrmAppEntity
from app.domain.app_platform import CrmAppPlatformEntity

TCommand = TypeVar("TCommand", bound=BaseModel)


class SdkCommandMapper:
    @staticmethod
    def _to_command(command_type: type[TCommand], payload: Mapping[str, object]) -> TCommand:
        return command_type.model_validate(dict(payload))

    @classmethod
    def install_from_transport(cls, payload: Mapping[str, object]) -> SdkInstallCommand:
        return cls._to_command(SdkInstallCommand, payload)

    @classmethod
    def events_from_transport(cls, payload: Mapping[str, object]) -> SdkEventsCommand:
        return cls._to_command(SdkEventsCommand, payload)

    @classmethod
    def params_update_from_transport(cls, payload: Mapping[str, object]) -> SdkParamsUpdateCommand:
        return cls._to_command(SdkParamsUpdateCommand, payload)

    @classmethod
    def push_register_from_transport(cls, payload: Mapping[str, object]) -> SdkPushRegisterCommand:
        return cls._to_command(SdkPushRegisterCommand, payload)

    @classmethod
    def config_from_transport(cls, payload: Mapping[str, object]) -> GetSdkConfigCommand:
        return cls._to_command(GetSdkConfigCommand, payload)


class SdkDomainMapper:
    @staticmethod
    def _to_string_list(value: object) -> list[str]:
        if value is None:
            return []
        if isinstance(value, list):
            return [str(item) for item in value if item is not None]
        if isinstance(value, Mapping):
            items = value.get("items")
            if isinstance(items, list):
                return [str(item) for item in items if item is not None]
            return [str(item) for item in value.values() if item is not None]
        return [str(value)]

    @classmethod
    def app_from_command(cls, command: SdkCreateAppCommand) -> CrmAppEntity:
        return CrmAppEntity(
            app_id=command.id,
            name=command.name,
            code_slug=command.code_slug,
            description=command.description,
            tech_description=command.tech_description,
            logo_url=command.logo_ur,
            screenshots=cls._to_string_list(command.screanshots),
        )    
        
    @classmethod
    def app_platform_from_command(cls, command: SdkCreateAppPlatformCommand) -> CrmAppPlatformEntity:
        return CrmAppPlatformEntity(
            app_id=command.app_id,
            platform=command.platform,
            package_name=command.package_name,
            install_key=command.install_key,
            store_url=command.store_url,
            sdk_public_key=command.sdk_public_key,
            sdk_secret_hash=command.sdk_secret_hash,
            status=command.status,
            platform_id=command.platform_id,
            created_at=command.created_at,
            updated_at=command.updated_at,
        )
