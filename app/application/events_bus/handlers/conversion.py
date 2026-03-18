from app.application.exceptions import ApplicationError
from app.domain.conversion_definition.CrmConversionDefinitionEntity import (
    CrmConversionDefinitionEntity,
)
from app.domain.event_bus.entity import DomainEventMessage
from app.domain.event_bus.events.crm_events import ConversionEventMessage
from app.domain.event_bus.service_protocol import AsyncEventMessageHandler
from app.domain.uow import UnitOfWorkFacotyProtocol, UnitOfWorkProtocol


class AsyncConversionHandler(AsyncEventMessageHandler):
    def __init__(self, uow_factory: UnitOfWorkFacotyProtocol) -> None:
        self.__uow_factory = uow_factory

    @staticmethod
    def _get_definition_lookup(
        uow: UnitOfWorkProtocol,
        *,
        app_id: int | None,
        click_id: str,
    ) -> dict[str, CrmConversionDefinitionEntity]:
        definitions = uow.conversion_definition_repo.list_by_app_id(app_id)

        if not definitions:
            raise ApplicationError(
                "AsyncConversionHandler could not find conversion definitions "
                f"for app_id='{app_id}' and click_id='{click_id}'"
            )

        return {
            definition.machine_key: definition
            for definition in definitions
        }

    async def handle(self, message: DomainEventMessage) -> None:
        if not isinstance(message, ConversionEventMessage):
            raise ApplicationError(
                "AsyncConversionHandler expected ConversionEventMessage, "
                f"got {type(message).__name__}"
            )

        with self.__uow_factory.create() as uow:
            click = uow.click_repo.get_by_id(message.click_id)

            if click is None:
                raise ApplicationError(
                    f"AsyncConversionHandler could not find click with id='{message.click_id}'"
                )

            app_platform = uow.app_platform_repo.get_by_id(click.app_platform_id)

            if app_platform is None:
                raise ApplicationError(
                    "AsyncConversionHandler could not find app platform "
                    f"with id='{click.app_platform_id}' for click_id='{message.click_id}'"
                )

            definition_lookup = self._get_definition_lookup(
                uow,
                app_id=app_platform.app_id,
                click_id=message.click_id,
            )
            definition = definition_lookup.get(message.event_key)

            if definition is None:
                raise ApplicationError(
                    "AsyncConversionHandler could not find conversion definition "
                    f"for event_key='{message.event_key}' app_id='{app_platform.app_id}' "
                    f"and click_id='{message.click_id}'"
                )

            has_amount = message.amount is not None
            has_currency = message.currency is not None
            has_amount_usd = message.amount_usd is not None
            has_revenue_payload = has_amount or has_currency or has_amount_usd

            if has_revenue_payload and not definition.revenue_enabled:
                raise ApplicationError(
                    "AsyncConversionHandler conversion definition "
                    f"for event_key='{message.event_key}' does not allow revenue fields "
                    f"for app_id='{app_platform.app_id}' and click_id='{message.click_id}'"
                )

            if definition.expects_amount and not has_amount:
                raise ApplicationError(
                    "AsyncConversionHandler conversion definition "
                    f"for event_key='{message.event_key}' requires amount "
                    f"for click_id='{message.click_id}'"
                )

            if definition.expects_currency and not has_currency:
                raise ApplicationError(
                    "AsyncConversionHandler conversion definition "
                    f"for event_key='{message.event_key}' requires currency "
                    f"for click_id='{message.click_id}'"
                )

            if has_amount and not definition.expects_amount:
                raise ApplicationError(
                    "AsyncConversionHandler conversion definition "
                    f"for event_key='{message.event_key}' does not accept amount "
                    f"for click_id='{message.click_id}'"
                )

            if has_currency and not definition.expects_currency:
                raise ApplicationError(
                    "AsyncConversionHandler conversion definition "
                    f"for event_key='{message.event_key}' does not accept currency "
                    f"for click_id='{message.click_id}'"
                )

            if has_amount_usd and not (has_amount and has_currency):
                raise ApplicationError(
                    "AsyncConversionHandler conversion message "
                    f"for event_key='{message.event_key}' requires amount and currency "
                    "when amount_usd is present"
                )
