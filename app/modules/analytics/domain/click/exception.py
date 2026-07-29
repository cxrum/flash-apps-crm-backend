from app.modules.analytics.core.exception import AnalyticsDomainException


class AnalyticsClickStatusInvalid(AnalyticsDomainException):
    def __init__(self) -> None:
        super().__init__("domain.click.status.invalid", {}, 400)


class AnalyticsClickPlatformMismatch(AnalyticsDomainException):
    def __init__(self) -> None:
        super().__init__("domain.click.platform.invalid", {}, 400)
