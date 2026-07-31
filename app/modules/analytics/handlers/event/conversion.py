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
                "analytics.handler.conversion.definitions.not_found",
                {"app_id": app_id, "click_id": click_id},
            )

        return {definition.machine_key: definition for definition in definitions}

    async def handle(self, message: EventMessage) -> None:
        if not isinstance(message, ConversionEventMessage):
            raise GeneralException(
                "analytics.handler.conversion.message.invalid",
                {"message_type": type(message).__name__},
            )

        with self.__uow_factory.create() as uow:
            click = uow.click_repo.get_by_id(message.click_id)

            if click is None:
                raise GeneralException("analytics.handler.conversion.click.not_found", {"click_id": message.click_id})

            app_platform = uow.app_platform_repo.get_by_id(click.app_platform_id)

            if app_platform is None or app_platform.platform_id is None:
                raise GeneralException(
                    "analytics.handler.conversion.platform.not_found",
                    {"app_platform_id": click.app_platform_id, "click_id": message.click_id},
                )

            definition_lookup = self._get_definition_lookup(
                uow,
                app_id=app_platform.app_id,
                click_id=message.click_id,
            )
            definition = definition_lookup.get(message.event_key)

            if definition is None:
                raise GeneralException(
                    "analytics.handler.conversion.definition.not_found",
                    {"event_key": message.event_key, "app_id": app_platform.app_id, "click_id": message.click_id},
                )

            has_amount = message.amount is not None
            has_currency = message.currency is not None
            has_amount_usd = message.amount_usd is not None
            has_revenue_payload = has_amount or has_currency or has_amount_usd

            if has_revenue_payload and not definition.revenue_enabled:
                raise GeneralException(
                    "analytics.handler.conversion.revenue_fields.forbidden",
                    {"event_key": message.event_key, "app_id": app_platform.app_id, "click_id": message.click_id},
                )

            if definition.expects_amount and not has_amount:
                raise GeneralException(
                    "analytics.handler.conversion.amount.required",
                    {"event_key": message.event_key, "click_id": message.click_id},
                )

            if definition.expects_currency and not has_currency:
                raise GeneralException(
                    "analytics.handler.conversion.currency.required",
                    {"event_key": message.event_key, "click_id": message.click_id},
                )

            if has_amount and not definition.expects_amount:
                raise GeneralException(
                    "analytics.handler.conversion.amount.unexpected",
                    {"event_key": message.event_key, "click_id": message.click_id},
                )

            if has_currency and not definition.expects_currency:
                raise GeneralException(
                    "analytics.handler.conversion.currency.unexpected",
                    {"event_key": message.event_key, "click_id": message.click_id},
                )

            if has_amount_usd and not (has_amount and has_currency):
                raise GeneralException(
                    "analytics.handler.conversion.amount_usd.dependencies.invalid",
                    {"event_key": message.event_key},
                )

            StatisticAggregates.update(
                uow=uow, message=message, revenue_enabled=definition.revenue_enabled, app_platform=app_platform
            )
