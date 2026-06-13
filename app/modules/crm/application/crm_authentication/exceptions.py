from typing import Any, Dict

from app.core.exception import BaseBoundaryException
from app.modules.crm.core.exception_resolver import MessageResolver


class AuthenticationException(BaseBoundaryException):
    def __init__(self, message_key: str = "internal", context: Dict[str, Any] = {}, code: int = 500):
        super().__init__(message_key, context, code)
        self.args = (MessageResolver().resolve(message_key, context),)


class InvalidOrExpiredToken(AuthenticationException):
    def __init__(self):
        super().__init__("authentication.token.invalid_or_expired", {}, 401)


class InvalidPasswordOrEmail(AuthenticationException):
    def __init__(self):
        super().__init__("authentication.credentials.invalid", {}, 401)


class EmailIsExist(AuthenticationException):
    def __init__(self):
        super().__init__("authentication.email.exists", {}, 409)
