from app.modules.crm.domain.exceptions import DomainException


class AnalyticsClickStatusInvalid(DomainException):
    def __init__(self) -> None:
        super().__init__("domain.click.status.invalid", {}, 400)


class AnalyticsClickPlatformMismatch(DomainException):
    def __init__(self) -> None:
        super().__init__("domain.click.platform.invalid", {}, 400)
