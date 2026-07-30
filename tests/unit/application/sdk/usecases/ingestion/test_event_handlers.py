from __future__ import annotations

import asyncio
from datetime import UTC, datetime

import pytest
from app.modules.crm.domain.event_bus.entity import DomainEventMessage

from app.modules.analytics.handlers.event.conversion import AsyncConversionHandler
from app.modules.analytics.handlers.event.event import ConversionEventMessage, MetricEventMessage
from app.modules.analytics.handlers.event.metric import AsyncMetricHandler
from app.modules.analytics.handlers.update_param.event import UpdateCurrentParamMessage
from app.modules.analytics.handlers.update_param.update_param import AsyncUpdateParamHandler
from app.modules.crm.application.events_bus.handlers.audit import AsyncAuditValueHandler
from app.modules.analytics.core.exception import AnalyticsApplicationException as GeneralException
from app.modules.analytics.di.event_bus import get_event_subscribers as get_analytics_event_subscribers
from app.modules.crm.di.event_bus import get_event_subscribers as get_crm_event_subscribers
from app.modules.crm.domain.app.CrmAppEntity import CrmAppEntity
from app.modules.crm.domain.app_platform.CrmAppPlatformEntity import CrmAppPlatformEntity
from app.modules.analytics.domain.click.AnalyticsClickEntity import AnalyticsClickEntity
from app.modules.crm.domain.event_bus.events.crm_value_update_event import ValueChangedEvent
from app.modules.crm.domain.exceptions import DomainException
from tests.unit.builders import build_app_entity, build_app_platform_entity, build_click_entity
from tests.unit.builders.entities import (
    build_conversion_definition_entity,
    build_metric_definition_entity,
    build_param_definition_entity,
)
from tests.unit.doubles.domain.uow import StubUnitOfWork, StubUoWFactory


def _seed_click_context(
    uow: StubUnitOfWork,
    *,
    app_id: int = 1,
    click_id: str = "click-1",
) -> tuple[CrmAppEntity, CrmAppPlatformEntity, AnalyticsClickEntity]:
    app = uow.app_repo.save(build_app_entity(app_id=app_id))
    platform = uow.app_platform_repo.save(build_app_platform_entity(app_id=app.app_id, platform="ios"))
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
            "payload": {"geo": "UK"},
            "created_at": occurred_at,
        },
        occurred_at=occurred_at,
    )


def _build_conversion_message(
    *,
    click_id: str = "click-1",
    event_id: str = "conversion-event-1",
    event_key: str = "purchase",
    amount: object | None = None,
    currency: object | None = None,
    amount_usd: object | None = None,
    payload: object | None = None,
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
            "payload": {} if payload is None else payload,
            "created_at": occurred_at,
        },
        occurred_at=occurred_at,
    )


def _seed_conversion_handler_context(
    uow: StubUnitOfWork,
    *,
    app_id: int = 1,
    click_id: str = "click-1",
    event_key: str = "purchase",
    revenue_enabled: bool = False,
    expects_amount: bool = False,
    expects_currency: bool = False,
    param_definitions: list[dict[str, object]] | None = None,
) -> tuple[CrmAppEntity, CrmAppPlatformEntity, AnalyticsClickEntity]:
    app, platform, click = _seed_click_context(
        uow,
        app_id=app_id,
        click_id=click_id,
    )
    uow.param_definition_repo.save_many(
        [
            build_param_definition_entity(app_id=app.app_id, **definition)
            for definition in (
                param_definitions
                or [{"display_name": "GEO", "machine_key": "geo", "data_type": "string", "groupable": True}]
            )
        ]
    )
    uow.conversion_definition_repo.save(
        build_conversion_definition_entity(
            app_id=app.app_id,
            machine_key=event_key,
            revenue_enabled=revenue_enabled,
            expects_amount=expects_amount,
            expects_currency=expects_currency,
        )
    )
    return app, platform, click


def test_async_metric_handler_accepts_valid_metric_event() -> None:
    async def scenario() -> None:
        uow = StubUnitOfWork()
        handler = AsyncMetricHandler(StubUoWFactory(uow))
        app, _, click = _seed_click_context(uow)

        uow.param_definition_repo.save_many(
            [
                build_param_definition_entity(
                    display_name="First open",
                    machine_key="first_open",
                    data_type="string",
                    app_id=app.app_id,
                    groupable=True,
                ),
                build_param_definition_entity(
                    display_name="Geo", machine_key="geo", data_type="string", app_id=app.app_id, groupable=True
                ),
            ]
        )

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
            GeneralException,
            match="expected MetricEventMessage, got DomainEventMessage",
        ):
            await handler.handle(DomainEventMessage(name=MetricEventMessage.EVENT_NAME))

    asyncio.run(scenario())


def test_async_metric_handler_rejects_missing_click_with_detailed_text() -> None:
    async def scenario() -> None:
        uow = StubUnitOfWork()
        handler = AsyncMetricHandler(StubUoWFactory(uow))

        with pytest.raises(
            GeneralException,
            match="could not find click with id='missing-click'",
        ):
            await handler.handle(_build_metric_message(click_id="missing-click"))

    asyncio.run(scenario())


def test_async_metric_handler_rejects_missing_app_platform_with_detailed_text() -> None:
    async def scenario() -> None:
        uow = StubUnitOfWork()
        handler = AsyncMetricHandler(StubUoWFactory(uow))
        click = uow.click_repo.insert(build_click_entity(click_id="click-without-platform", app_platform_id=999))

        with pytest.raises(
            GeneralException,
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
            GeneralException,
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
            GeneralException,
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
            GeneralException,
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
            GeneralException,
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
        _, platform, click = _seed_conversion_handler_context(uow)

        await handler.handle(
            _build_conversion_message(
                click_id=click.click_id,
                payload={"geo": "UK"},
            )
        )

        assert platform.platform_id is not None

        aggeregates = uow.statistics_repo.list_by_app_platform_id(platform.platform_id)

        assert uow.enter_count == 1
        assert uow.commit_count == 1
        assert uow.rollback_count == 0
        assert len(aggeregates) == 1
        assert aggeregates[0].amount_usd is None
        assert aggeregates[0].count == 1
        assert aggeregates[0].geo == "UK"

    asyncio.run(scenario())


def test_async_conversion_handler_accepts_valid_revenue_conversion_event() -> None:
    async def scenario() -> None:
        uow = StubUnitOfWork()
        handler = AsyncConversionHandler(StubUoWFactory(uow))
        _, platform, click = _seed_conversion_handler_context(
            uow,
            revenue_enabled=True,
            expects_amount=True,
            expects_currency=True,
            param_definitions=[
                {"display_name": "GEO", "machine_key": "geo", "data_type": "string", "groupable": True},
                {"display_name": "UTM", "machine_key": "utm_source", "data_type": "string", "groupable": True},
            ],
        )

        payload = {
            "geo": "UK",
            "utm_source": "facebook",
        }

        await handler.handle(
            _build_conversion_message(
                click_id=click.click_id,
                amount=5.0,
                currency="USD",
                amount_usd=5.0,
                payload=payload,
            )
        )

        await handler.handle(
            _build_conversion_message(
                click_id=click.click_id,
                amount=2.0,
                currency="USD",
                amount_usd=2.0,
                payload=payload,
            )
        )

        await handler.handle(
            _build_conversion_message(
                click_id=click.click_id,
                amount=-2.0,
                currency="USD",
                amount_usd=-2.0,
                payload=payload,
            )
        )

        assert platform.platform_id is not None

        aggeregates = uow.statistics_repo.list_by_app_platform_id(platform.platform_id)
        detailed_aggeregates = uow.custom_params_statistics_repo.list_by_app_platform_id(platform.platform_id)
        detailed_by_key = {item.param_key: item for item in detailed_aggeregates}

        assert uow.enter_count == 3
        assert uow.commit_count == 3
        assert uow.rollback_count == 0
        assert len(aggeregates) == 1
        assert aggeregates[0].amount_usd == 5.0
        assert aggeregates[0].count == 3
        assert aggeregates[0].geo == "UK"

        assert len(detailed_by_key) == 2
        assert detailed_by_key["geo"].param_value == "UK"
        assert detailed_by_key["utm_source"].param_value == "facebook"
        assert all(item.count == 3 for item in detailed_by_key.values())

    asyncio.run(scenario())


def test_async_conversion_handler_accepts_multiple_payload_value_types_and_ignores_unknown_params() -> None:
    async def scenario() -> None:
        uow = StubUnitOfWork()
        handler = AsyncConversionHandler(StubUoWFactory(uow))
        _, platform, click = _seed_conversion_handler_context(
            uow,
            param_definitions=[
                {"display_name": "GEO", "machine_key": "geo", "data_type": "string", "groupable": True},
                {"display_name": "Attempt", "machine_key": "attempt", "data_type": "integer", "groupable": True},
                {"display_name": "Score", "machine_key": "score", "data_type": "float", "groupable": True},
                {"display_name": "Premium", "machine_key": "premium", "data_type": "boolean", "groupable": True},
            ],
        )

        await handler.handle(
            _build_conversion_message(
                click_id=click.click_id,
                payload={
                    "geo": "DE",
                    "attempt": "2",
                    "score": "4.5",
                    "premium": "yes",
                    "ignored": "skip-me",
                },
            )
        )

        assert platform.platform_id is not None

        aggeregates = uow.statistics_repo.list_by_app_platform_id(platform.platform_id)
        detailed_aggeregates = uow.custom_params_statistics_repo.list_by_app_platform_id(platform.platform_id)
        detailed_by_key = {item.param_key: item for item in detailed_aggeregates}

        assert len(aggeregates) == 1
        assert aggeregates[0].geo == "DE"
        assert set(detailed_by_key) == {"geo", "attempt", "score", "premium"}
        assert detailed_by_key["geo"].param_value == "DE"
        assert detailed_by_key["attempt"].param_value == "2"
        assert detailed_by_key["score"].param_value == "4.5"
        assert detailed_by_key["premium"].param_value == "True"

    asyncio.run(scenario())


@pytest.mark.parametrize("geo_key", ["geo"])
def test_async_conversion_handler_uses_geo_alias_param_definitions(
    geo_key: str,
) -> None:
    async def scenario() -> None:
        uow = StubUnitOfWork()
        handler = AsyncConversionHandler(StubUoWFactory(uow))
        _, platform, click = _seed_conversion_handler_context(
            uow,
            param_definitions=[
                {"display_name": geo_key.upper(), "machine_key": geo_key, "data_type": "string", "groupable": True}
            ],
        )

        await handler.handle(
            _build_conversion_message(
                click_id=click.click_id,
                payload={geo_key: "BR"},
            )
        )

        assert platform.platform_id is not None

        aggeregates = uow.statistics_repo.list_by_app_platform_id(platform.platform_id)
        detailed_aggeregates = uow.custom_params_statistics_repo.list_by_app_platform_id(platform.platform_id)

        assert len(aggeregates) == 1
        assert aggeregates[0].geo == "BR"
        assert len(detailed_aggeregates) == 1
        assert detailed_aggeregates[0].param_key == geo_key
        assert detailed_aggeregates[0].param_value == "BR"

    asyncio.run(scenario())


def test_async_conversion_handler_tracks_multiple_custom_params_across_repeated_events() -> None:
    async def scenario() -> None:
        uow = StubUnitOfWork()
        handler = AsyncConversionHandler(StubUoWFactory(uow))
        _, platform, click = _seed_conversion_handler_context(
            uow,
            param_definitions=[
                {"display_name": "GEO", "machine_key": "geo", "data_type": "string", "groupable": True},
                {"display_name": "UTM Source", "machine_key": "utm_source", "data_type": "string", "groupable": True},
                {"display_name": "Campaign", "machine_key": "campaign", "data_type": "string", "groupable": True},
                {"display_name": "Ad Group", "machine_key": "ad_group", "data_type": "string", "groupable": True},
                {"display_name": "Premium", "machine_key": "premium", "data_type": "boolean", "groupable": True},
            ],
        )
        payload = {
            "geo": "CA",
            "utm_source": "google",
            "campaign": "spring-sale",
            "ad_group": "retargeting",
            "premium": True,
        }

        await handler.handle(
            _build_conversion_message(
                click_id=click.click_id,
                payload=payload,
            )
        )
        await handler.handle(
            _build_conversion_message(
                click_id=click.click_id,
                payload=payload,
            )
        )

        assert platform.platform_id is not None

        aggeregates = uow.statistics_repo.list_by_app_platform_id(platform.platform_id)
        detailed_aggeregates = uow.custom_params_statistics_repo.list_by_app_platform_id(platform.platform_id)
        detailed_by_key = {item.param_key: item for item in detailed_aggeregates}

        assert len(aggeregates) == 1
        assert aggeregates[0].count == 2
        assert set(detailed_by_key) == {"geo", "utm_source", "campaign", "ad_group", "premium"}
        assert all(item.count == 2 for item in detailed_by_key.values())
        assert detailed_by_key["premium"].param_value == "True"

    asyncio.run(scenario())


def test_async_conversion_handler_rejects_invalid_payload_shape() -> None:
    async def scenario() -> None:
        uow = StubUnitOfWork()
        handler = AsyncConversionHandler(StubUoWFactory(uow))
        _, _, click = _seed_conversion_handler_context(uow)

        with pytest.raises(TypeError, match="payload must be a dict"):
            await handler.handle(
                _build_conversion_message(
                    click_id=click.click_id,
                    payload=["geo", "UK"],
                )
            )

    asyncio.run(scenario())


@pytest.mark.parametrize(
    ("field_name", "invalid_value"),
    [
        ("amount", "five"),
        ("amount_usd", object()),
    ],
)
def test_async_conversion_handler_rejects_invalid_money_value_classes(
    field_name: str,
    invalid_value: object,
) -> None:
    async def scenario() -> None:
        uow = StubUnitOfWork()
        handler = AsyncConversionHandler(StubUoWFactory(uow))
        _, _, click = _seed_conversion_handler_context(
            uow,
            revenue_enabled=True,
            expects_amount=True,
            expects_currency=True,
        )

        message_kwargs: dict[str, object] = {
            "click_id": click.click_id,
            "amount": 5.0,
            "currency": "USD",
            "amount_usd": 5.0,
            "payload": {"geo": "UK"},
        }
        message_kwargs[field_name] = invalid_value

        with pytest.raises((TypeError, ValueError)):
            await handler.handle(_build_conversion_message(**message_kwargs))  # type: ignore

    asyncio.run(scenario())


def test_async_conversion_handler_rejects_invalid_value_for_param_definition() -> None:
    async def scenario() -> None:
        uow = StubUnitOfWork()
        handler = AsyncConversionHandler(StubUoWFactory(uow))
        _, _, click = _seed_conversion_handler_context(
            uow,
            param_definitions=[
                {"display_name": "GEO", "machine_key": "geo", "data_type": "string", "groupable": True},
                {"display_name": "Attempt", "machine_key": "attempt", "data_type": "integer", "groupable": True},
            ],
        )

        with pytest.raises(DomainException, match="Param 'attempt' expected integer, got 'not-an-integer'"):
            await handler.handle(
                _build_conversion_message(
                    click_id=click.click_id,
                    payload={
                        "geo": "UK",
                        "attempt": "not-an-integer",
                    },
                )
            )

    asyncio.run(scenario())


def test_async_conversion_handler_rejects_wrong_message_type_with_detailed_text() -> None:
    async def scenario() -> None:
        handler = AsyncConversionHandler(StubUoWFactory(StubUnitOfWork()))

        with pytest.raises(
            GeneralException,
            match="expected ConversionEventMessage, got DomainEventMessage",
        ):
            await handler.handle(DomainEventMessage(name=ConversionEventMessage.EVENT_NAME))

    asyncio.run(scenario())


def test_async_conversion_handler_rejects_missing_click_with_detailed_text() -> None:
    async def scenario() -> None:
        uow = StubUnitOfWork()
        handler = AsyncConversionHandler(StubUoWFactory(uow))

        with pytest.raises(
            GeneralException,
            match="could not find click with id='missing-click'",
        ):
            await handler.handle(_build_conversion_message(click_id="missing-click"))

    asyncio.run(scenario())


def test_async_conversion_handler_rejects_missing_app_platform_with_detailed_text() -> None:
    async def scenario() -> None:
        uow = StubUnitOfWork()
        handler = AsyncConversionHandler(StubUoWFactory(uow))
        click = uow.click_repo.insert(build_click_entity(click_id="click-without-platform", app_platform_id=999))

        with pytest.raises(
            GeneralException,
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
            GeneralException,
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
            GeneralException,
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
            GeneralException,
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

        with pytest.raises(GeneralException, match=expected_match):
            await handler.handle(
                _build_conversion_message(
                    click_id=click.click_id,
                    **message_overrides,  # type: ignore
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

        with pytest.raises(GeneralException, match=expected_match):
            await handler.handle(
                _build_conversion_message(
                    click_id=click.click_id,
                    **message_overrides,  # type: ignore
                )
            )

    asyncio.run(scenario())


def test_event_subscribers_are_split_between_crm_and_analytics_buses() -> None:
    crm_subscriber_map = {event_name: type(handler) for event_name, handler in get_crm_event_subscribers()}
    analytics_subscriber_map = {
        event_name: type(handler) for event_name, handler in get_analytics_event_subscribers()
    }

    assert analytics_subscriber_map == {
        UpdateCurrentParamMessage.EVENT_NAME: AsyncUpdateParamHandler,
        MetricEventMessage.EVENT_NAME: AsyncMetricHandler,
        ConversionEventMessage.EVENT_NAME: AsyncConversionHandler,
    }
    assert crm_subscriber_map == {
        ValueChangedEvent.EVENT_NAME: AsyncAuditValueHandler,
    }
