from app.core.bus.contract import AsyncEventMessageHandler
from app.core.bus.type import EventMessage
from app.modules.analytics.application.ingestion.update_statistic import StatisticAggregates
from app.modules.analytics.domain.uow import AnalyticsUnitOfWorkFactoryProtocol, AnalyticsUnitOfWorkProtocol
from app.modules.analytics.handlers.event.event import MetricEventMessage
from app.modules.analytics.core.exception import AnalyticsApplicationException as GeneralException
from app.modules.crm.domain.metric_definition.CrmMetricDefinitionEntity import CrmMetricDefinitionEntity


class AsyncMetricHandler(AsyncEventMessageHandler):
    def __init__(self, uow_factory: AnalyticsUnitOfWorkFactoryProtocol) -> None:
        self.__uow_factory = uow_factory

    @staticmethod
    def _get_definition_lookup(
        uow: AnalyticsUnitOfWorkProtocol,
        *,
        app_id: int | None,
        click_id: str,
    ) -> dict[str, CrmMetricDefinitionEntity]:
        definitions = uow.metric_definition_repo.list_by_app_id(app_id)

        if not definitions:
            raise GeneralException(
                "analytics.handler.metric.definitions.not_found",
                {"app_id": app_id, "click_id": click_id},
            )

        return {definition.machine_key: definition for definition in definitions}

    async def handle(self, message: EventMessage) -> None:
        if not isinstance(message, MetricEventMessage):
            raise GeneralException(
                "analytics.handler.metric.message.invalid",
                {"message_type": type(message).__name__},
            )

        with self.__uow_factory.create() as uow:
            click = uow.click_repo.get_by_id(message.click_id)

            if click is None:
                raise GeneralException("analytics.handler.metric.click.not_found", {"click_id": message.click_id})

            app_platform = uow.app_platform_repo.get_by_id(click.app_platform_id)

            if app_platform is None or app_platform.platform_id is None:
                raise GeneralException(
                    "analytics.handler.metric.platform.not_found",
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
                    "analytics.handler.metric.definition.not_found",
                    {"event_key": message.event_key, "app_id": app_platform.app_id, "click_id": message.click_id},
                )

            if not definition.enabled:
                raise GeneralException(
                    "analytics.handler.metric.definition.disabled",
                    {"event_key": message.event_key, "app_id": app_platform.app_id, "click_id": message.click_id},
                )

            if message.amount is not None or message.currency is not None or message.amount_usd is not None:
                raise GeneralException(
                    "analytics.handler.metric.revenue_fields.invalid",
                    {"event_id": message.event_id, "click_id": message.click_id},
                )

            StatisticAggregates.update(uow=uow, message=message, revenue_enabled=False, app_platform=app_platform)
