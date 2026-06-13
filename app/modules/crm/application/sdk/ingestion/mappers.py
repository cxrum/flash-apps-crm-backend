from collections.abc import Mapping

from app.modules.crm.application.admin.push.commands import PushDeviceRegisterCommand
from app.modules.crm.application.sdk.apps.commands import AppConfigurationCommand
from app.modules.crm.application.sdk.ingestion.commands import (
    SdkEventsCommand,
    SdkInstallCommand,
    SdkParamsUpdateCommand,
    SdkPushStartCommand,
)
from app.modules.crm.core.utils.general_mapper import GeneralMapper


class SdkIngestionCommandMapper:
    @classmethod
    def install_from_transport(cls, payload: Mapping[str, object]) -> SdkInstallCommand:
        return GeneralMapper.command_payload_to_command(SdkInstallCommand, payload)

    @classmethod
    def config_from_transport(cls, payload: Mapping[str, object]) -> AppConfigurationCommand:
        return GeneralMapper.command_payload_to_command(AppConfigurationCommand, payload)

    @classmethod
    def events_from_transport(cls, payload: Mapping[str, object]) -> SdkEventsCommand:
        return GeneralMapper.command_payload_to_command(SdkEventsCommand, payload)

    @classmethod
    def params_update_from_transport(cls, payload: Mapping[str, object]) -> SdkParamsUpdateCommand:
        return GeneralMapper.command_payload_to_command(SdkParamsUpdateCommand, payload)
