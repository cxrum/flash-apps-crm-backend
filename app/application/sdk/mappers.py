from __future__ import annotations

from typing import Mapping, TypeVar

from pydantic import BaseModel

from app.application.sdk.entities import (
    GetSdkConfigCommand,
    SdkEventsCommand,
    SdkInstallCommand,
    SdkParamsUpdateCommand,
    SdkPushRegisterCommand,
)

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
