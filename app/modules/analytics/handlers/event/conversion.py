from app.core.bus.contract import AsyncEventMessageHandler
from app.core.bus.type import EventMessage
from app.modules.analytics.application.ingestion.update_statistic import StatisticAggregates
from app.modules.analytics.domain.uow import AnalyticsUnitOfWorkFactoryProtocol, AnalyticsUnitOfWorkProtocol
from app.modules.analytics.handlers.event.event import ConversionEventMessage
from app.modules.analytics.core.exception import AnalyticsApplicationException as GeneralException
from app.modules.crm.domain.conversion_definition.CrmConversionDefinitionEntity import (
    CrmConversionDefinitionEntity,
)


class AsyncConversionHandler(AsyncEventMessageHandler):
    def __init__(self, uow_factory: AnalyticsUnitOfWorkFactoryProtocol) -> None:
        self.__uow_factory = uow_factory

    @staticmethod
    def _get_definition_lookup(
        uow: AnalyticsUnitOfWorkProtocol,
        *,
        app_id: int | None,
        click_id: str,
    ) -> dict[str, CrmConversionDefinitionEntity]:
        definitions = uow.conversion_definition_repo.list_by_app_id(app_id)

        if not definitions:
            raise GeneralException(
                "AsyncConversionHandler could not find conversion definitions "
                f"for app_id='{app_id}' and click_id='{click_id}'"
            )

        return {definition.machine_key: definition for definition in definitions}

    async def handle(self, message: EventMessage) -> None:
        if not isinstance(message, ConversionEventMessage):
            raise GeneralException(
                f"AsyncConversionHandler expected ConversionEventMessage, got {type(message).__name__}"
            )

        with self.__uow_factory.create() as uow:
            click = uow.click_repo.get_by_id(message.click_id)

            if click is None:
                raise GeneralException(f"AsyncConversionHandler could not find click with id='{message.click_id}'")

            app_platform = uow.app_platform_repo.get_by_id(click.app_platform_id)

            if app_platform is None or app_platform.platform_id is None:
                raise GeneralException(
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
                raise GeneralException(
                    "AsyncConversionHandler could not find conversion definition "
                    f"for event_key='{message.event_key}' app_id='{app_platform.app_id}' "
                    f"and click_id='{message.click_id}'"
                )

            has_amount = message.amount is not None
            has_currency = message.currency is not None
            has_amount_usd = message.amount_usd is not None
            has_revenue_payload = has_amount or has_currency or has_amount_usd

            if has_revenue_payload and not definition.revenue_enabled:
                raise GeneralException(
                    "AsyncConversionHandler conversion definition "
                    f"for event_key='{message.event_key}' does not allow revenue fields "
                    f"for app_id='{app_platform.app_id}' and click_id='{message.click_id}'"
                )

            if definition.expects_amount and not has_amount:
                raise GeneralException(
                    "AsyncConversionHandler conversion definition "
                    f"for event_key='{message.event_key}' requires amount "
                    f"for click_id='{message.click_id}'"
                )

            if definition.expects_currency and not has_currency:
                raise GeneralException(
                    "AsyncConversionHandler conversion definition "
                    f"for event_key='{message.event_key}' requires currency "
                    f"for click_id='{message.click_id}'"
                )

            if has_amount and not definition.expects_amount:
                raise GeneralException(
                    "AsyncConversionHandler conversion definition "
                    f"for event_key='{message.event_key}' does not accept amount "
                    f"for click_id='{message.click_id}'"
                )

            if has_currency and not definition.expects_currency:
                raise GeneralException(
                    "AsyncConversionHandler conversion definition "
                    f"for event_key='{message.event_key}' does not accept currency "
                    f"for click_id='{message.click_id}'"
                )

            if has_amount_usd and not (has_amount and has_currency):
                raise GeneralException(
                    "AsyncConversionHandler conversion message "
                    f"for event_key='{message.event_key}' requires amount and currency "
                    "when amount_usd is present"
                )

            StatisticAggregates.update(
                uow=uow, message=message, revenue_enabled=definition.revenue_enabled, app_platform=app_platform
            )
