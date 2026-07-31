from app.core.bus.event.events.app_configuration import (
    AppConfigurationProjectionMessage,
    AppPlatformConfigurationProjectionMessage,
)
from app.modules.analytics.domain.app.AnalyticsAppEntity import AnalyticsAppEntity
from app.modules.analytics.domain.app_platform.AnalyticsAppPlatformEntity import AnalyticsAppPlatformEntity


class AnalyticsAppConfigurationProjectionMapper:
    @staticmethod
    def app_from_message(message: AppConfigurationProjectionMessage) -> AnalyticsAppEntity:
        return AnalyticsAppEntity(
            app_id=message.app_id,
            code_slug=message.code_slug,
        )

    @staticmethod
    def app_platform_from_message(
        message: AppPlatformConfigurationProjectionMessage,
    ) -> AnalyticsAppPlatformEntity:
        return AnalyticsAppPlatformEntity(
            platform_id=message.platform_id,
            app_id=message.app_id,
            platform=message.platform,
            install_key=message.install_key,
            sdk_secret_encrypted=message.sdk_secret_encrypted,
        )
