from typing import Any, Dict

from app.modules.crm.domain.exceptions import DomainException


class StatisticsAggregateException(DomainException):
    def __init__(self, message_key: str = "internal", context: Dict[str, Any] = {}, code: int = 400):
        super().__init__(message_key, context, code)


class InvalidStatisticsAmountCurrency(StatisticsAggregateException):
    def __init__(self):
        super().__init__("domain.statistics.amount.currency.invalid", {}, 400)
