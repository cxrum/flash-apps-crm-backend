from datetime import date, datetime
import json
from typing import Any

from app.application.events_bus.factories.param_update_event import UpdateParamMessageFactory, UpdateParamValue
from app.application.sdk.ingestion.update_statistic import StatisticAggregates
from app.application.exceptions import ApplicationError
from app.domain.custom_params_statistics_aggregate.CustomParamsStatisticsAggregateEntity import CustomParamsStatisticsAggregateEntity
from app.domain.event_bus.entity import DomainEventMessage
from app.domain.event_bus.events.crm_events import MetricEventMessage
from app.domain.event_bus.service_protocol import AsyncEventMessageHandler, IAsyncEventBus
from app.domain.metric_definition.CrmMetricDefinitionEntity import CrmMetricDefinitionEntity
from app.domain.param_definition.CrmParamDefinitionEntity import CrmParamDefinitionEntity
from app.domain.statistics_aggregate import StatisticsAggregateEntity
from app.domain.uow import UnitOfWorkFactoryProtocol, UnitOfWorkProtocol


class AsyncMetricHandler(AsyncEventMessageHandler):
    def __init__(self, uow_factory: UnitOfWorkFactoryProtocol) -> None:
        self.__uow_factory = uow_factory

    @staticmethod
    def _get_definition_lookup(
        uow: UnitOfWorkProtocol,
        *,
        app_id: int | None,
        click_id: str,
    ) -> dict[str, CrmMetricDefinitionEntity]:
        definitions = uow.metric_definition_repo.list_by_app_id(app_id)

        if not definitions:
            raise ApplicationError(
                "AsyncMetricHandler could not find metric definitions "
                f"for app_id='{app_id}' and click_id='{click_id}'"
            )

        return {
            definition.machine_key: definition
            for definition in definitions
        }

    async def handle(self, message: DomainEventMessage) -> None:
        if not isinstance(message, MetricEventMessage):
            raise ApplicationError(
                "AsyncMetricHandler expected MetricEventMessage, "
                f"got {type(message).__name__}"
            )

        with self.__uow_factory.create() as uow:
            click = uow.click_repo.get_by_id(message.click_id)

            if click is None:
                raise ApplicationError(
                    f"AsyncMetricHandler could not find click with id='{message.click_id}'"
                )

            app_platform = uow.app_platform_repo.get_by_id(click.app_platform_id)

            if app_platform is None or app_platform.platform_id is None:
                raise ApplicationError(
                    "AsyncMetricHandler could not find app platform "
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
                    "AsyncMetricHandler could not find metric definition "
                    f"for event_key='{message.event_key}' app_id='{app_platform.app_id}' "
                    f"and click_id='{message.click_id}'"
                )

            if not definition.enabled:
                raise ApplicationError(
                    "AsyncMetricHandler metric definition "
                    f"for event_key='{message.event_key}' is disabled "
                    f"for app_id='{app_platform.app_id}' and click_id='{message.click_id}'"
                )

            if (
                message.amount is not None
                or message.currency is not None
                or message.amount_usd is not None
            ):
                raise ApplicationError(
                    "AsyncMetricHandler metric events do not support revenue fields "
                    f"for event_id='{message.event_id}' and click_id='{message.click_id}'"
                )

            StatisticAggregates.update(
                uow=uow,
                message=message,
                revenue_enabled=False,
                app_platform=app_platform
            )
