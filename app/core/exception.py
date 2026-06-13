from typing import Any, Dict


class BaseBoundaryException(Exception):
    def __init__(self, message_key: str, context: Dict[str, Any], code: int):
        self.message_key = message_key
        self.context = context
        self.code = code
        super().__init__(f"Key: {message_key}, Context: {context}")


class BusException(Exception):
    def __init__(self, message: str, context: Dict[str, Any] = {}):
        super().__init__(message)
