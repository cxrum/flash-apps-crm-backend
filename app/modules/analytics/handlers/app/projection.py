from app.core.bus.contract import AsyncEventMessageHandler
from app.core.bus.event.events.app_configuration import (
    AppConfigurationProjectionMessage,
    AppPlatformConfigurationProjectionMessage,
)
from app.core.bus.type import EventMessage
from app.modules.analytics.core.exception import AnalyticsApplicationException
from app.modules.analytics.domain.uow import AnalyticsUnitOfWorkFactoryProtocol
from app.modules.analytics.handlers.app.mapper import AnalyticsAppConfigurationProjectionMapper


class AppConfigurationProjectionHandler(AsyncEventMessageHandler):
    def __init__(self, uow_factory: AnalyticsUnitOfWorkFactoryProtocol) -> None:
        self._uow_factory = uow_factory

    async def handle(self, message: EventMessage) -> None:
        if not isinstance(message, AppConfigurationProjectionMessage):
            raise AnalyticsApplicationException(
                "analytics.projection.app.message.invalid",
                {"message_type": type(message).__name__},
            )

        with self._uow_factory.create() as uow:
            uow.app_repo.save(AnalyticsAppConfigurationProjectionMapper.app_from_message(message))


class AppPlatformConfigurationProjectionHandler(AsyncEventMessageHandler):
    def __init__(self, uow_factory: AnalyticsUnitOfWorkFactoryProtocol) -> None:
        self._uow_factory = uow_factory

    async def handle(self, message: EventMessage) -> None:
        if not isinstance(message, AppPlatformConfigurationProjectionMessage):
            raise AnalyticsApplicationException(
                "analytics.projection.app_platform.message.invalid",
                {"message_type": type(message).__name__},
            )

        with self._uow_factory.create() as uow:
            uow.app_platform_repo.save(AnalyticsAppConfigurationProjectionMapper.app_platform_from_message(message))
