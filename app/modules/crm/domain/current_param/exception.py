from typing import Any, Dict

from app.modules.crm.domain.exceptions import DomainException


class CurrentParamsException(DomainException):
    def __init__(self, message_key: str = "internal", context: Dict[str, Any] = {}, code: int = 400):
        super().__init__(message_key, context, code)


class UnsupportedCurrentParamUpdatePolicy(CurrentParamsException):
    def __init__(self, update_policy: str):
        super().__init__(
            "domain.current_param.update_policy.unsupported",
            {"update_policy": update_policy},
            400,
        )


class AppendPolicyNotSupported(CurrentParamsException):
    def __init__(self):
        super().__init__("domain.current_param.append.unsupported", {}, 400)


class MergePolicyNotSupported(CurrentParamsException):
    def __init__(self):
        super().__init__("domain.current_param.merge.unsupported", {}, 400)
