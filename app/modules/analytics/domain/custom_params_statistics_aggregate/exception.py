from app.modules.analytics.core.exception import AnalyticsDomainException


class AnalyticsCustomParamsStatisticsAmountCurrencyInvalid(AnalyticsDomainException):
    def __init__(self) -> None:
        super().__init__("domain.custom_params_statistics.amount.currency.invalid", {}, 400)
