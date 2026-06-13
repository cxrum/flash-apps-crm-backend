from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime

from app.modules.crm.domain.currency.entity import Money
from app.modules.crm.domain.custom_params_statistics_aggregate.exception import (
    InvalidCustomParamsStatisticsAmountCurrency,
)


@dataclass()
class CustomParamsStatisticsAggregateEntity:
    app_platform_id: int
    geo: str
    ddate: date
    event_type: str
    event_key: str
    param_key: str
    param_value: str
    count: int
    aggregate_id: int | None = None
    amount_usd: float | None = None
    updated_at: datetime | None = None
    created_at: datetime | None = None

    def increase_count(self) -> None:
        self.count += 1

    def increase_amount_usd(self, amount: Money):
        if amount.base != "USD":
            raise InvalidCustomParamsStatisticsAmountCurrency()

        self.amount_usd = self.amount_usd if self.amount_usd is not None else 0.0
        self.amount_usd += amount.value

    def decrease_amount_usd(self, amount: Money):
        if amount.base != "USD":
            raise InvalidCustomParamsStatisticsAmountCurrency()

        self.amount_usd = self.amount_usd if self.amount_usd is not None else 0.0
        self.amount_usd -= amount.value
