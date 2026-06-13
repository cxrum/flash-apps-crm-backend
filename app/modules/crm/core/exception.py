from typing import Any, Dict

from app.core.exception import BaseBoundaryException


class CrmExceptionBase(BaseBoundaryException):
    def __init__(self, message_key: str, context: Dict[str, Any], code: int):
        super().__init__(message_key, context, code)
