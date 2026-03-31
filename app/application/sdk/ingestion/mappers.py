from app.application.sdk.apps.commands import AppConfigurationCommand
from app.application.sdk.ingestion.commands import SdkEventsCommand, SdkInstallCommand, SdkParamsUpdateCommand, SdkPushRegisterCommand, SdkPushStartCommand
from app.core.utils.general_mapper import GeneralMapper


from collections.abc import Mapping


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

    @classmethod
    def push_register_from_transport(cls, payload: Mapping[str, object]) -> SdkPushRegisterCommand:
        return GeneralMapper.command_payload_to_command(SdkPushRegisterCommand, payload)
    
    @classmethod
    def push_start_from_transport(cls, payload: Mapping[str, object]) -> SdkPushStartCommand:
        return GeneralMapper.command_payload_to_command(SdkPushStartCommand, payload)
