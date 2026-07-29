from __future__ import annotations

import asyncio
from collections.abc import Sequence

from app.core.bus.event.events.analytics import ConversionEventMessage, MetricEventMessage
from app.core.bus.type import EventMessage
from app.modules.analytics.application.ingestion.service import IngestionService
from app.modules.analytics.handlers.update_param.event import UpdateCurrentParamMessage
from app.modules.crm.domain.app_platform.CrmAppPlatformEntity import CrmAppPlatformEntity
from tests.unit.base import UnitTestContext
from tests.unit.builders import (
    build_app_entity,
    build_app_platform_entity,
    build_click_entity,
    build_sdk_event_command,
    build_sdk_events_command,
    build_sdk_install_command,
    build_sdk_params_update_command,
)


class RecordingAsyncEventBus:
    def __init__(self) -> None:
        self.messages: list[EventMessage] = []

    async def publish(self, message: EventMessage) -> None:
        self.messages.append(message)

    async def publish_many(self, messages: Sequence[EventMessage]) -> None:
        self.messages.extend(messages)


def _build_service(context: UnitTestContext, bus: RecordingAsyncEventBus) -> IngestionService:
    return IngestionService(
        uow_factory=context.uow_factory,
        async_event_bus=bus,
        currency_service=context.currency_service,
        idempotency_repo=context.idempotency_repository,
    )


def _seed_platform(context: UnitTestContext) -> CrmAppPlatformEntity:
    context.uow.app_repo.save(build_app_entity(app_id=1))
    return context.uow.app_platform_repo.save(build_app_platform_entity(app_id=1, install_key="install-key-ios"))


def test_install_publishes_the_persisted_install_event_once(unit_test_context: UnitTestContext) -> None:
    async def scenario() -> None:
        bus = RecordingAsyncEventBus()
        service = _build_service(unit_test_context, bus)
        platform = _seed_platform(unit_test_context)
        command = build_sdk_install_command(
            click_id=None,
            install_key=platform.install_key,
            idempotency_key="install-event-message",
        )

        response = await service.process_install(command)

        assert response is not None
        assert len(bus.messages) == 1
        message = bus.messages[0]
        assert isinstance(message, MetricEventMessage)
        assert message.event_id == command.idempotency_key
        assert message.click_id == response.click_id
        assert message.event_key == "install"
        assert message.raw_payload["install_key"] == platform.install_key
        assert message.metadata == {"source": "sdk"}

        assert await service.process_install(command) is None
        assert len(bus.messages) == 1

    asyncio.run(scenario())


def test_batch_publishes_only_accepted_events_with_their_business_type(
    unit_test_context: UnitTestContext,
) -> None:
    async def scenario() -> None:
        bus = RecordingAsyncEventBus()
        service = _build_service(unit_test_context, bus)
        platform = _seed_platform(unit_test_context)
        click = unit_test_context.uow.click_repo.insert(
            build_click_entity(app_platform_id=platform.platform_id or 0)
        )
        command = build_sdk_events_command(
            click_id=click.click_id,
            idempotency_key="event-batch-message",
            events=[
                build_sdk_event_command(idempotency_key="metric-event", type="metric", key="opened"),
                build_sdk_event_command(idempotency_key="conversion-event", type="conversion", key="purchase"),
                build_sdk_event_command(idempotency_key="metric-event", type="metric", key="ignored-duplicate"),
            ],
        )

        assert await service.process_batch_events(command)

        assert [type(message) for message in bus.messages] == [MetricEventMessage, ConversionEventMessage]
        assert [message.event_key for message in bus.messages] == ["opened", "purchase"]
        assert [message.event_id for message in bus.messages] == ["metric-event", "conversion-event"]
        assert all(message.click_id == click.click_id for message in bus.messages)

    asyncio.run(scenario())


def test_parameter_update_publishes_the_current_params_request(unit_test_context: UnitTestContext) -> None:
    async def scenario() -> None:
        bus = RecordingAsyncEventBus()
        service = _build_service(unit_test_context, bus)
        platform = _seed_platform(unit_test_context)
        click = unit_test_context.uow.click_repo.insert(
            build_click_entity(app_platform_id=platform.platform_id or 0)
        )
        command = build_sdk_params_update_command(
            click_id=click.click_id,
            idempotency_key="params-event-message",
            params={"campaign": "summer"},
        )

        assert await service.update_params(command)

        assert len(bus.messages) == 1
        message = bus.messages[0]
        assert isinstance(message, UpdateCurrentParamMessage)
        assert message.click_id == click.click_id
        assert message.params == {"campaign": "summer"}
        assert message.updated_at == command.event_time
        assert message.metadata == {"source": "sdk"}

    asyncio.run(scenario())
