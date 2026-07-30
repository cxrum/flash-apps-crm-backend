from app.modules.analytics.core.exception import AnalyticsDomainException


class UnsupportedCurrentParamUpdatePolicy(AnalyticsDomainException):
    def __init__(self, update_policy: str) -> None:
        super().__init__("domain.current_param.update_policy.unsupported", {"update_policy": update_policy}, 400)


class AppendPolicyNotSupported(AnalyticsDomainException):
    def __init__(self) -> None:
        super().__init__("domain.current_param.append.unsupported", {}, 400)


class MergePolicyNotSupported(AnalyticsDomainException):
    def __init__(self) -> None:
        super().__init__("domain.current_param.merge.unsupported", {}, 400)
