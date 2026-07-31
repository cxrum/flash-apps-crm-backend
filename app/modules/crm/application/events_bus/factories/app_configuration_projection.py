from app.core.bus.event.events.app_configuration import (
    AppConfigurationProjectionMessage,
    AppPlatformConfigurationProjectionMessage,
)
from app.modules.crm.domain.app.CrmAppEntity import CrmAppEntity
from app.modules.crm.domain.app_platform.CrmAppPlatformEntity import CrmAppPlatformEntity


class AppConfigurationProjectionMessageFactory:
    @staticmethod
    def from_app(entity: CrmAppEntity) -> AppConfigurationProjectionMessage:
        if entity.app_id is None:
            raise ValueError("App configuration projection requires an app_id")

        return AppConfigurationProjectionMessage(
            name=AppConfigurationProjectionMessage.EVENT_NAME,
            payload={
                "app_id": entity.app_id,
                "code_slug": entity.code_slug,
            },
            metadata={"source": "crm"},
        )

    @staticmethod
    def from_app_platform(
        entity: CrmAppPlatformEntity,
    ) -> AppPlatformConfigurationProjectionMessage:
        if entity.platform_id is None:
            raise ValueError("App platform configuration projection requires a platform_id")

        return AppPlatformConfigurationProjectionMessage(
            name=AppPlatformConfigurationProjectionMessage.EVENT_NAME,
            payload={
                "platform_id": entity.platform_id,
                "app_id": entity.app_id,
                "platform": entity.platform,
                "install_key": entity.install_key,
                "sdk_secret_encrypted": entity.sdk_secret_encrypted,
            },
            metadata={"source": "crm"},
        )
