from app.modules.analytics.application.logs.mappers import AnalyticsLogsMapper
from app.modules.analytics.domain.click.AnalyticsClickEntity import AnalyticsClickEntity
from tests.unit.builders import build_analytics_event_entity


def test_analytics_logs_mapper_maps_analytics_click_and_event_entities() -> None:
    click = AnalyticsClickEntity(
        click_id="click-1",
        app_platform_id=7,
        raw_query={"campaign": "spring"},
        normalized_params={"utm_source": "partner"},
    )
    event = build_analytics_event_entity(
        event_id="event-1",
        click_id=click.click_id,
        event_key="purchase",
    )

    click_value = AnalyticsLogsMapper.click_log_from_domain(click)
    event_value = AnalyticsLogsMapper.event_log_from_domain(event)

    assert click_value.click_id == click.click_id
    assert click_value.normalized_params == {"utm_source": "partner"}
    assert event_value.event_id == event.event_id
    assert event_value.event_key == "purchase"
