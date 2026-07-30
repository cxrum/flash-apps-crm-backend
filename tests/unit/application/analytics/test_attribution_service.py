from app.modules.analytics.application.attribution.service import AnalyticsAttributionService
from tests.unit.builders import (
    build_click_entity,
    build_current_param_entity,
    build_event_entity,
    build_install_entity,
)
from tests.unit.doubles.domain.uow import StubUnitOfWork, StubUoWFactory


def test_postback_context_contains_only_the_attribution_data_needed_by_other_modules() -> None:
    uow = StubUnitOfWork()
    uow.click_repo.insert(build_click_entity(click_id="click-1", app_platform_id=7))
    uow.install_repo.save(build_install_entity(click_id="click-1", install_id=12, app_user_id=23))
    uow.event_repo.insert(
        build_event_entity(
            event_id="event-1",
            click_id="click-1",
            payload={"order_id": "order-1"},
            amount=15.0,
            amount_usd=10.0,
        )
    )
    uow.current_param_repo.save(
        build_current_param_entity(
            click_id="click-1",
            param_key="utm_source",
            value_string="partner",
        )
    )
    service = AnalyticsAttributionService(StubUoWFactory(uow))

    context = service.get_postback_context("event-1")

    assert context is not None
    assert context.event_id == "event-1"
    assert context.click.click_id == "click-1"
    assert context.click.app_platform_id == 7
    assert context.click.install_id == 12
    assert context.click.app_user_id == 23
    assert context.payload == {"order_id": "order-1"}
    assert context.current_params == {"utm_source": "partner"}


def test_postback_context_is_unavailable_when_the_event_or_its_click_is_missing() -> None:
    uow = StubUnitOfWork()
    uow.event_repo.insert(build_event_entity(event_id="orphan-event", click_id="missing-click"))
    service = AnalyticsAttributionService(StubUoWFactory(uow))

    assert service.get_postback_context("missing-event") is None
    assert service.get_postback_context("orphan-event") is None
