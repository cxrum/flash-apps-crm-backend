from dataclasses import dataclass
from datetime import date, datetime

from app.modules.analytics.domain.statistics_aggregate.exception import AnalyticsStatisticsAmountCurrencyInvalid
from app.modules.analytics.domain.currency.entity import Money


@dataclass
class AnalyticsStatisticsAggregateEntity:
    app_platform_id: int
    geo: str
    ddate: date
    event_type: str
    event_key: str
    count: int
    aggregate_id: int | None = None
    amount_usd: float | None = None
    updated_at: datetime | None = None
    created_at: datetime | None = None

    def increase_count(self) -> None:
        self.count += 1

    def increase_amount_usd(self, amount: Money) -> None:
        if amount.base != "USD":
            raise AnalyticsStatisticsAmountCurrencyInvalid()
        self.amount_usd = (self.amount_usd or 0.0) + amount.value
