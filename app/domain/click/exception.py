from typing import Any, Dict

from app.domain.exceptions import DomainException


class ClickException(DomainException):
    def __init__(self, message_key: str = "internal", context: Dict[str, Any]={}, code: int = 400):
        super().__init__(message_key, context, code)


class IncorrectClickStatus(ClickException):
    def __init__(self):
        super().__init__("domain.click.status.invalid", {}, 400)


class IncorrectClickPlatform(ClickException):
    def __init__(self):
        super().__init__("domain.click.platform.invalid", {}, 400)
