from app.modules.analytics.core.exception import AnalyticsDomainException


class AnalyticsStatisticsAmountCurrencyInvalid(AnalyticsDomainException):
    def __init__(self):
        super().__init__("domain.statistics.amount.currency.invalid", {}, 400)
