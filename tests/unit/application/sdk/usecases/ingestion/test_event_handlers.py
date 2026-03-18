from __future__ import annotations

import asyncio
from datetime import UTC, datetime

import pytest

from app.application.events_bus.handlers.conversion import AsyncConversionHandler
from app.application.events_bus.handlers.metric import AsyncMetricHandler
from app.application.events_bus.handlers.update_param import AsyncUpdateParamHandler
from app.application.exceptions import ApplicationError
from app.di.dependencies import get_event_subscribers
from app.domain.event_bus.entity import DomainEventMessage
from app.domain.event_bus.events.crm_events import ConversionEventMessage, MetricEventMessage
from app.domain.event_bus.events.crm_update_params import UpdateCurrentParamMessage
from tests.unit.builders import build_app_entity, build_app_platform_entity, build_click_entity
from tests.unit.builders.entities import (
    build_conversion_definition_entity,
    build_metric_definition_entity,
)
from tests.unit.doubles.domain.uow import StubUnitOfWork, StubUoWFactory


def _seed_click_context(
    uow: StubUnitOfWork,
    *,
    app_id: int = 1,
    click_id: str = "click-1",
) -> tuple[object, object, object]:
    app = uow.app_repo.save(build_app_entity(app_id=app_id))
    platform = uow.app_platform_repo.save(
        build_app_platform_entity(app_id=app.app_id, platform="ios")
    )
    click = uow.click_repo.insert(
        build_click_entity(
            click_id=click_id,
            app_platform_id=platform.platform_id or 0,
        )
    )
    return app, platform, click


def _build_metric_message(
    *,
    click_id: str = "click-1",
    event_id: str = "metric-event-1",
    event_key: str = "first_open",
    amount: float | None = None,
    currency: str | None = None,
    amount_usd: float | None = None,
) -> MetricEventMessage:
    occurred_at = datetime(2026, 3, 18, 12, 0, tzinfo=UTC)
    return MetricEventMessage(
        name=MetricEventMessage.EVENT_NAME,
        payload={
            "event_id": event_id,
            "click_id": click_id,
            "event_type": "metric",
            "event_key": event_key,
            "app_user_id": None,
            "amount": amount,
            "currency": currency,
            "amount_usd": amount_usd,
            "event_time_utc": occurred_at,
            "payload": {},
            "created_at": occurred_at,
        },
        occurred_at=occurred_at,
    )


def _build_conversion_message(
    *,
    click_id: str = "click-1",
    event_id: str = "conversion-event-1",
    event_key: str = "purchase",
    amount: float | None = None,
    currency: str | None = None,
    amount_usd: float | None = None,
) -> ConversionEventMessage:
    occurred_at = datetime(2026, 3, 18, 12, 0, tzinfo=UTC)
    return ConversionEventMessage(
        name=ConversionEventMessage.EVENT_NAME,
        payload={
            "event_id": event_id,
            "click_id": click_id,
            "event_type": "conversion",
            "event_key": event_key,
            "app_user_id": None,
            "amount": amount,
            "currency": currency,
            "amount_usd": amount_usd,
            "event_time_utc": occurred_at,
            "payload": {},
            "created_at": occurred_at,
        },
        occurred_at=occurred_at,
    )


def test_async_metric_handler_accepts_valid_metric_event() -> None:
    async def scenario() -> None:
        uow = StubUnitOfWork()
        handler = AsyncMetricHandler(StubUoWFactory(uow))
        app, _, click = _seed_click_context(uow)
        uow.metric_definition_repo.save(
            build_metric_definition_entity(
                app_id=app.app_id,
                machine_key="first_open",
                enabled=True,
            )
        )

        await handler.handle(_build_metric_message(click_id=click.click_id))

        assert uow.enter_count == 1
        assert uow.commit_count == 1
        assert uow.rollback_count == 0

    asyncio.run(scenario())


def test_async_metric_handler_rejects_wrong_message_type_with_detailed_text() -> None:
    async def scenario() -> None:
        handler = AsyncMetricHandler(StubUoWFactory(StubUnitOfWork()))

        with pytest.raises(
            ApplicationError,
            match="expected MetricEventMessage, got DomainEventMessage",
        ):
            await handler.handle(DomainEventMessage(name=MetricEventMessage.EVENT_NAME))

    asyncio.run(scenario())


def test_async_metric_handler_rejects_missing_click_with_detailed_text() -> None:
    async def scenario() -> None:
        uow = StubUnitOfWork()
        handler = AsyncMetricHandler(StubUoWFactory(uow))

        with pytest.raises(
            ApplicationError,
            match="could not find click with id='missing-click'",
        ):
            await handler.handle(_build_metric_message(click_id="missing-click"))

    asyncio.run(scenario())


def test_async_metric_handler_rejects_missing_app_platform_with_detailed_text() -> None:
    async def scenario() -> None:
        uow = StubUnitOfWork()
        handler = AsyncMetricHandler(StubUoWFactory(uow))
        click = uow.click_repo.insert(
            build_click_entity(click_id="click-without-platform", app_platform_id=999)
        )

        with pytest.raises(
            ApplicationError,
            match=f"could not find app platform with id='{click.app_platform_id}' for click_id='{click.click_id}'",
        ):
            await handler.handle(_build_metric_message(click_id=click.click_id))

    asyncio.run(scenario())


def test_async_metric_handler_rejects_missing_metric_definitions_with_detailed_text() -> None:
    async def scenario() -> None:
        uow = StubUnitOfWork()
        handler = AsyncMetricHandler(StubUoWFactory(uow))
        app, _, click = _seed_click_context(uow)

        with pytest.raises(
            ApplicationError,
            match=f"could not find metric definitions for app_id='{app.app_id}' and click_id='{click.click_id}'",
        ):
            await handler.handle(_build_metric_message(click_id=click.click_id))

    asyncio.run(scenario())


def test_async_metric_handler_rejects_unknown_event_key_with_detailed_text() -> None:
    async def scenario() -> None:
        uow = StubUnitOfWork()
        handler = AsyncMetricHandler(StubUoWFactory(uow))
        app, _, click = _seed_click_context(uow)
        uow.metric_definition_repo.save(
            build_metric_definition_entity(
                app_id=app.app_id,
                machine_key="install",
            )
        )

        with pytest.raises(
            ApplicationError,
            match=f"could not find metric definition for event_key='first_open' app_id='{app.app_id}' and click_id='{click.click_id}'",
        ):
            await handler.handle(_build_metric_message(click_id=click.click_id))

    asyncio.run(scenario())


def test_async_metric_handler_rejects_disabled_metric_definition() -> None:
    async def scenario() -> None:
        uow = StubUnitOfWork()
        handler = AsyncMetricHandler(StubUoWFactory(uow))
        app, _, click = _seed_click_context(uow)
        uow.metric_definition_repo.save(
            build_metric_definition_entity(
                app_id=app.app_id,
                machine_key="first_open",
                enabled=False,
            )
        )

        with pytest.raises(
            ApplicationError,
            match="metric definition .* is disabled",
        ):
            await handler.handle(_build_metric_message(click_id=click.click_id))

    asyncio.run(scenario())


def test_async_metric_handler_rejects_money_fields() -> None:
    async def scenario() -> None:
        uow = StubUnitOfWork()
        handler = AsyncMetricHandler(StubUoWFactory(uow))
        app, _, click = _seed_click_context(uow)
        uow.metric_definition_repo.save(
            build_metric_definition_entity(
                app_id=app.app_id,
                machine_key="first_open",
            )
        )

        with pytest.raises(
            ApplicationError,
            match="metric events do not support revenue fields",
        ):
            await handler.handle(
                _build_metric_message(
                    click_id=click.click_id,
                    amount=1.0,
                    currency="USD",
                    amount_usd=1.0,
                )
            )

    asyncio.run(scenario())


def test_async_conversion_handler_accepts_valid_non_revenue_conversion_event() -> None:
    async def scenario() -> None:
        uow = StubUnitOfWork()
        handler = AsyncConversionHandler(StubUoWFactory(uow))
        app, _, click = _seed_click_context(uow)
        uow.conversion_definition_repo.save(
            build_conversion_definition_entity(
                app_id=app.app_id,
                machine_key="purchase",
            )
        )

        await handler.handle(_build_conversion_message(click_id=click.click_id))

        assert uow.enter_count == 1
        assert uow.commit_count == 1
        assert uow.rollback_count == 0

    asyncio.run(scenario())


def test_async_conversion_handler_accepts_valid_revenue_conversion_event() -> None:
    async def scenario() -> None:
        uow = StubUnitOfWork()
        handler = AsyncConversionHandler(StubUoWFactory(uow))
        app, _, click = _seed_click_context(uow)
        uow.conversion_definition_repo.save(
            build_conversion_definition_entity(
                app_id=app.app_id,
                machine_key="purchase",
                revenue_enabled=True,
                expects_amount=True,
                expects_currency=True,
            )
        )

        await handler.handle(
            _build_conversion_message(
                click_id=click.click_id,
                amount=5.0,
                currency="USD",
                amount_usd=5.0,
            )
        )

        assert uow.enter_count == 1
        assert uow.commit_count == 1
        assert uow.rollback_count == 0

    asyncio.run(scenario())


def test_async_conversion_handler_rejects_wrong_message_type_with_detailed_text() -> None:
    async def scenario() -> None:
        handler = AsyncConversionHandler(StubUoWFactory(StubUnitOfWork()))

        with pytest.raises(
            ApplicationError,
            match="expected ConversionEventMessage, got DomainEventMessage",
        ):
            await handler.handle(DomainEventMessage(name=ConversionEventMessage.EVENT_NAME))

    asyncio.run(scenario())


def test_async_conversion_handler_rejects_missing_click_with_detailed_text() -> None:
    async def scenario() -> None:
        uow = StubUnitOfWork()
        handler = AsyncConversionHandler(StubUoWFactory(uow))

        with pytest.raises(
            ApplicationError,
            match="could not find click with id='missing-click'",
        ):
            await handler.handle(_build_conversion_message(click_id="missing-click"))

    asyncio.run(scenario())


def test_async_conversion_handler_rejects_missing_app_platform_with_detailed_text() -> None:
    async def scenario() -> None:
        uow = StubUnitOfWork()
        handler = AsyncConversionHandler(StubUoWFactory(uow))
        click = uow.click_repo.insert(
            build_click_entity(click_id="click-without-platform", app_platform_id=999)
        )

        with pytest.raises(
            ApplicationError,
            match=f"could not find app platform with id='{click.app_platform_id}' for click_id='{click.click_id}'",
        ):
            await handler.handle(_build_conversion_message(click_id=click.click_id))

    asyncio.run(scenario())


def test_async_conversion_handler_rejects_missing_conversion_definitions_with_detailed_text() -> None:
    async def scenario() -> None:
        uow = StubUnitOfWork()
        handler = AsyncConversionHandler(StubUoWFactory(uow))
        app, _, click = _seed_click_context(uow)

        with pytest.raises(
            ApplicationError,
            match=f"could not find conversion definitions for app_id='{app.app_id}' and click_id='{click.click_id}'",
        ):
            await handler.handle(_build_conversion_message(click_id=click.click_id))

    asyncio.run(scenario())


def test_async_conversion_handler_rejects_unknown_event_key_with_detailed_text() -> None:
    async def scenario() -> None:
        uow = StubUnitOfWork()
        handler = AsyncConversionHandler(StubUoWFactory(uow))
        app, _, click = _seed_click_context(uow)
        uow.conversion_definition_repo.save(
            build_conversion_definition_entity(
                app_id=app.app_id,
                machine_key="signup",
            )
        )

        with pytest.raises(
            ApplicationError,
            match=f"could not find conversion definition for event_key='purchase' app_id='{app.app_id}' and click_id='{click.click_id}'",
        ):
            await handler.handle(_build_conversion_message(click_id=click.click_id))

    asyncio.run(scenario())


def test_async_conversion_handler_rejects_revenue_fields_when_definition_disallows_them() -> None:
    async def scenario() -> None:
        uow = StubUnitOfWork()
        handler = AsyncConversionHandler(StubUoWFactory(uow))
        app, _, click = _seed_click_context(uow)
        uow.conversion_definition_repo.save(
            build_conversion_definition_entity(
                app_id=app.app_id,
                machine_key="purchase",
                revenue_enabled=False,
            )
        )

        with pytest.raises(
            ApplicationError,
            match="does not allow revenue fields",
        ):
            await handler.handle(
                _build_conversion_message(
                    click_id=click.click_id,
                    amount=5.0,
                )
            )

    asyncio.run(scenario())


@pytest.mark.parametrize(
    ("definition_overrides", "message_overrides", "expected_match"),
    [
        (
            {"revenue_enabled": True, "expects_amount": True, "expects_currency": False},
            {"currency": None},
            "requires amount",
        ),
        (
            {"revenue_enabled": True, "expects_amount": False, "expects_currency": True},
            {"amount": None},
            "requires currency",
        ),
    ],
)
def test_async_conversion_handler_rejects_missing_required_fields(
    definition_overrides: dict[str, bool],
    message_overrides: dict[str, float | str | None],
    expected_match: str,
) -> None:
    async def scenario() -> None:
        uow = StubUnitOfWork()
        handler = AsyncConversionHandler(StubUoWFactory(uow))
        app, _, click = _seed_click_context(uow)
        uow.conversion_definition_repo.save(
            build_conversion_definition_entity(
                app_id=app.app_id,
                machine_key="purchase",
                **definition_overrides,
            )
        )

        with pytest.raises(ApplicationError, match=expected_match):
            await handler.handle(
                _build_conversion_message(
                    click_id=click.click_id,
                    **message_overrides,
                )
            )

    asyncio.run(scenario())


@pytest.mark.parametrize(
    ("definition_overrides", "message_overrides", "expected_match"),
    [
        (
            {"revenue_enabled": True, "expects_amount": False, "expects_currency": False},
            {"amount": 5.0},
            "does not accept amount",
        ),
        (
            {"revenue_enabled": True, "expects_amount": False, "expects_currency": False},
            {"currency": "USD"},
            "does not accept currency",
        ),
    ],
)
def test_async_conversion_handler_rejects_unexpected_revenue_fields(
    definition_overrides: dict[str, bool],
    message_overrides: dict[str, float | str | None],
    expected_match: str,
) -> None:
    async def scenario() -> None:
        uow = StubUnitOfWork()
        handler = AsyncConversionHandler(StubUoWFactory(uow))
        app, _, click = _seed_click_context(uow)
        uow.conversion_definition_repo.save(
            build_conversion_definition_entity(
                app_id=app.app_id,
                machine_key="purchase",
                **definition_overrides,
            )
        )

        with pytest.raises(ApplicationError, match=expected_match):
            await handler.handle(
                _build_conversion_message(
                    click_id=click.click_id,
                    **message_overrides,
                )
            )

    asyncio.run(scenario())


def test_get_event_subscribers_includes_update_param_metric_and_conversion_handlers() -> None:
    subscriber_map = {
        event_name: type(handler)
        for event_name, handler in get_event_subscribers()
    }

    assert subscriber_map == {
        UpdateCurrentParamMessage.EVENT_NAME: AsyncUpdateParamHandler,
        MetricEventMessage.EVENT_NAME: AsyncMetricHandler,
        ConversionEventMessage.EVENT_NAME: AsyncConversionHandler,
    }
