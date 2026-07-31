from app.core.bus.type import EventMessage


class AppConfigurationProjectionMessage(EventMessage):
    EVENT_NAME = "analytics.app.configuration.projection.requested"

    @property
    def app_id(self) -> int:
        return int(self.payload["app_id"])

    @property
    def code_slug(self) -> str:
        return str(self.payload["code_slug"])


class AppPlatformConfigurationProjectionMessage(EventMessage):
    EVENT_NAME = "analytics.app-platform.configuration.projection.requested"

    @property
    def platform_id(self) -> int:
        return int(self.payload["platform_id"])

    @property
    def app_id(self) -> int:
        return int(self.payload["app_id"])

    @property
    def platform(self) -> str:
        return str(self.payload["platform"])

    @property
    def install_key(self) -> str:
        return str(self.payload["install_key"])

    @property
    def sdk_secret_encrypted(self) -> str:
        return str(self.payload["sdk_secret_encrypted"])
