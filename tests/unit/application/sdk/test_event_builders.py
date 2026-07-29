from __future__ import annotations

from datetime import UTC, datetime

import pytest

from app.modules.analytics.core.exception import AnalyticsApplicationException
from app.modules.analytics.application.ingestion.event_builder import (
    ConversionEventBuilder,
    MetricsEventBuilder,
    RevenueEventBuilder,
)


def test_metrics_event_builder_builds_metric_without_money_fields() -> None:
    event = (
        MetricsEventBuilder(
            event_id="evt-metric-1",
            click_id="click-1",
            event_key="first_open",
            event_time_utc=datetime(2026, 3, 12, 12, 0, tzinfo=UTC),
            payload={"source": "sdk"},
        )
        ._set_amount(None)
        ._set_currency(None)
        ._set_amount_in_usd(None)
        .build()
    )

    assert event.event_type == "metric"
    assert event.amount is None
    assert event.currency is None
    assert event.amount_usd is None


def test_metrics_event_builder_rejects_money_values() -> None:
    builder = MetricsEventBuilder(
        event_id="evt-metric-2",
        click_id="click-1",
        event_key="session_start",
    )

    with pytest.raises(AnalyticsApplicationException, match="cannot carry money values"):
        builder._set_amount(9.99)


def test_revenue_event_builder_requires_amount_and_currency() -> None:
    builder = RevenueEventBuilder(
        event_id="evt-revenue-1",
        click_id="click-1",
        event_key="purchase",
    )

    with pytest.raises(AnalyticsApplicationException, match="require amount"):
        builder.build()


def test_revenue_event_builder_builds_conversion_with_money_fields() -> None:
    event = (
        RevenueEventBuilder(
            event_id="evt-revenue-2",
            click_id="click-1",
            event_key="purchase",
            payload={"product_id": "sku-1"},
        )
        ._set_amount(19.99)
        ._set_currency("usd")
        ._set_amount_in_usd(19.99)
        .build()
    )

    assert event.event_type == "conversion"
    assert event.amount == 19.99
    assert event.currency == "USD"
    assert event.amount_usd == 19.99


def test_conversion_event_builder_builds_non_revenue_conversion() -> None:
    event = (
        ConversionEventBuilder(
            event_id="evt-conversion-1",
            click_id="click-1",
            event_key="signup_complete",
            payload={"funnel_step": "done"},
        )
        ._set_amount(None)
        ._set_currency(None)
        ._set_amount_in_usd(None)
        .build()
    )

    assert event.event_type == "conversion"
    assert event.amount is None
    assert event.currency is None
    assert event.amount_usd is None


def test_conversion_event_builder_rejects_money_values() -> None:
    builder = ConversionEventBuilder(
        event_id="evt-conversion-2",
        click_id="click-1",
        event_key="signup_complete",
    )

    with pytest.raises(AnalyticsApplicationException, match="cannot carry money values"):
        builder._set_currency("USD")
