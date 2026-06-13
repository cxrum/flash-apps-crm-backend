from typing import Any, Dict

from app.modules.crm.domain.exceptions import DomainException


class CustomParamsStatisticsAggregateException(DomainException):
    def __init__(self, message_key: str = "internal", context: Dict[str, Any] = {}, code: int = 400):
        super().__init__(message_key, context, code)


class InvalidCustomParamsStatisticsAmountCurrency(CustomParamsStatisticsAggregateException):
    def __init__(self):
        super().__init__("domain.custom_params_statistics.amount.currency.invalid", {}, 400)
