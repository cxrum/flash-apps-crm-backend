from datetime import UTC, datetime

import pytest

from app.infra.analytics_attribution_adapter import CrmAnalyticsAttributionAdapter
from app.modules.analytics.application.attribution.contracts import AnalyticsClickContext, AnalyticsPostbackContext
from app.modules.analytics.application.attribution.service import AnalyticsAttributionService
from app.modules.crm.application.admin.exception import ClickNotFound, EventNotFound
from app.modules.crm.application.admin.postback.service import PostbackService
from app.modules.crm.application.admin.push.service import PushService
from app.modules.crm.domain.event_bus.service_protocol import IAsyncEventBus
from tests.unit.builders import (
    build_admin_evaluate_postback_rule_command,
    build_app_entity,
    build_app_platform_entity,
    build_click_entity,
    build_event_entity,
    build_install_entity,
    build_postback_rule_entity,
    build_sdk_push_register_command,
)
from tests.unit.doubles.application import StubS2SRequester
from tests.unit.doubles.domain.uow import StubUnitOfWork, StubUoWFactory


class _AnalyticsAttributionPortStub:
    def __init__(
        self,
        *,
        click_context: AnalyticsClickContext | None = None,
        postback_context: AnalyticsPostbackContext | None = None,
    ) -> None:
        self.click_context = click_context
        self.postback_context = postback_context

    def get_click_context(self, click_id: str) -> AnalyticsClickContext | None:
        return self.click_context if self.click_context is not None and self.click_context.click_id == click_id else None

    def get_postback_context(self, event_id: str) -> AnalyticsPostbackContext | None:
        return (
            self.postback_context
            if self.postback_context is not None and self.postback_context.event_id == event_id
            else None
        )


class _AuthorizationStub:
    def required_user_permission(self, **_: object) -> None:
        return None


def _analytics_gateway(uow: StubUnitOfWork) -> CrmAnalyticsAttributionAdapter:
    return CrmAnalyticsAttributionAdapter(AnalyticsAttributionService(StubUoWFactory(uow)))  # type: ignore[arg-type]


def test_attribution_adapter_maps_click_context_fields() -> None:
    analytics_context = AnalyticsClickContext(
        click_id="click-1",
        app_platform_id=3,
        install_id=9,
        app_user_id=12,
    )
    adapter = CrmAnalyticsAttributionAdapter(
        _AnalyticsAttributionPortStub(click_context=analytics_context)  # type: ignore[arg-type]
    )

    crm_context = adapter.get_click_context("click-1")

    assert crm_context is not None
    assert crm_context.click_id == "click-1"
    assert crm_context.app_platform_id == 3
    assert crm_context.install_id == 9
    assert crm_context.app_user_id == 12


def test_attribution_adapter_maps_postback_context_without_sharing_mutable_values() -> None:
    analytics_context = AnalyticsPostbackContext(
        event_id="event-1",
        click=AnalyticsClickContext("click-1", 3, 9, 12),
        event_type="conversion",
        event_key="purchase",
        event_time_utc=datetime(2026, 7, 30, 12, tzinfo=UTC),
        amount=10.5,
        amount_usd=10.0,
        payload={"order_id": "order-1"},
        current_params={"campaign": "summer"},
    )
    adapter = CrmAnalyticsAttributionAdapter(
        _AnalyticsAttributionPortStub(postback_context=analytics_context)  # type: ignore[arg-type]
    )

    crm_context = adapter.get_postback_context("event-1")

    assert crm_context is not None
    assert crm_context.event_id == "event-1"
    assert crm_context.click.click_id == "click-1"
    assert crm_context.click.app_platform_id == 3
    assert crm_context.click.install_id == 9
    assert crm_context.click.app_user_id == 12
    assert crm_context.event_type == "conversion"
    assert crm_context.event_key == "purchase"
    assert crm_context.event_time_utc == datetime(2026, 7, 30, 12, tzinfo=UTC)
    assert crm_context.amount == 10.5
    assert crm_context.amount_usd == 10.0

    crm_context.payload["order_id"] = "changed"
    crm_context.current_params["campaign"] = "changed"

    assert analytics_context.payload == {"order_id": "order-1"}
    assert analytics_context.current_params == {"campaign": "summer"}


@pytest.mark.parametrize(
    ("method_name", "identifier"),
    [
        pytest.param("get_click_context", "missing-click", id="click"),
        pytest.param("get_postback_context", "missing-event", id="postback"),
    ],
)
def test_attribution_adapter_preserves_missing_analytics_context(
    method_name: str,
    identifier: str,
) -> None:
    adapter = CrmAnalyticsAttributionAdapter(_AnalyticsAttributionPortStub())  # type: ignore[arg-type]

    result = getattr(adapter, method_name)(identifier)

    assert result is None


def test_analytics_attribution_adapter_supplies_crm_push_registration_context() -> None:
    uow = StubUnitOfWork()
    uow.app_repo.save(build_app_entity(app_id=1))
    platform = uow.app_platform_repo.save(build_app_platform_entity(app_id=1, install_key="install-key-ios"))
    click = uow.click_repo.insert(build_click_entity(click_id="click-1", app_platform_id=platform.platform_id or 0))
    install = uow.install_repo.save(
        build_install_entity(click_id=click.click_id, app_platform_id=platform.platform_id or 0)
    )
    service = PushService(
        StubUoWFactory(uow),
        _AuthorizationStub(),  # type: ignore[arg-type]
        _analytics_gateway(uow),
    )
    command = build_sdk_push_register_command()

    service.register_device(command)

    token = uow.push_token_repo.get_by_token(command.push_token)
    assert token is not None
    assert token.click_id == click.click_id
    assert token.install_id == install.install_id


def test_analytics_attribution_adapter_selects_postback_rules_for_event_context(
    async_event_bus: IAsyncEventBus,
) -> None:
    uow = StubUnitOfWork()
    uow.app_repo.save(build_app_entity(app_id=1))
    platform = uow.app_platform_repo.save(build_app_platform_entity(app_id=1))
    click = uow.click_repo.insert(build_click_entity(click_id="click-1", app_platform_id=platform.platform_id or 0))
    uow.install_repo.save(build_install_entity(click_id=click.click_id, app_platform_id=platform.platform_id or 0))
    event = uow.event_repo.insert(
        build_event_entity(
            event_id="event-1",
            click_id=click.click_id,
            event_type="conversion",
            event_key="purchase",
        )
    )
    expected_rule = uow.postback_rule_repo.save(
        build_postback_rule_entity(
            platform_app_id=platform.platform_id or 0,
            trigger_type="conversion",
            event_key="purchase",
        )
    )
    uow.postback_rule_repo.save(
        build_postback_rule_entity(
            platform_app_id=platform.platform_id or 0,
            trigger_type="metric",
            event_key="purchase",
        )
    )

    service = PostbackService(
        StubUoWFactory(uow),
        async_event_bus,
        StubS2SRequester(),
        _analytics_gateway(uow),
    )

    rules = service.evaluate(
        build_admin_evaluate_postback_rule_command(
            event_id=event.event_id,
            trigger_type="conversion",
            event_key="purchase",
        )
    )

    assert rules == [expected_rule]


def test_missing_analytics_click_becomes_the_crm_push_boundary_exception() -> None:
    uow = StubUnitOfWork()
    service = PushService(
        StubUoWFactory(uow),
        _AuthorizationStub(),  # type: ignore[arg-type]
        _analytics_gateway(uow),
    )

    with pytest.raises(ClickNotFound):
        service.register_device(build_sdk_push_register_command(click_id="missing-click"))


def test_missing_analytics_event_becomes_the_crm_postback_boundary_exception(
    async_event_bus: IAsyncEventBus,
) -> None:
    uow = StubUnitOfWork()
    service = PostbackService(
        StubUoWFactory(uow),
        async_event_bus,
        StubS2SRequester(),
        _analytics_gateway(uow),
    )

    with pytest.raises(EventNotFound):
        service.evaluate(build_admin_evaluate_postback_rule_command(event_id="missing-event"))
