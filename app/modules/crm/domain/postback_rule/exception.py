from typing import Any, Dict

from app.modules.crm.domain.exceptions import DomainException


class PostbackRuleException(DomainException):
    def __init__(self, message_key: str = "internal", context: Dict[str, Any] = {}, code: int = 400):
        super().__init__(message_key, context, code)


class InvalidPostbackHttpMethod(PostbackRuleException):
    def __init__(self, http_method: str):
        super().__init__("domain.postback.http_method.invalid", {"http_method": http_method}, 400)


class MissingSecretTemplate(PostbackRuleException):
    def __init__(self, template_key: str):
        super().__init__("domain.postback.secret_template.missing", {"template_key": template_key}, 400)


class PostbackUrlRequired(PostbackRuleException):
    def __init__(self):
        super().__init__("domain.postback.url.required", {}, 400)


class PostbackUrlContainsSpaces(PostbackRuleException):
    def __init__(self):
        super().__init__("domain.postback.url.spaces", {}, 400)


class InvalidPostbackUrlScheme(PostbackRuleException):
    def __init__(self):
        super().__init__("domain.postback.url.scheme.invalid", {}, 400)


class MissingPostbackUrlHost(PostbackRuleException):
    def __init__(self):
        super().__init__("domain.postback.url.host.missing", {}, 400)


class InvalidPostbackTriggerType(PostbackRuleException):
    def __init__(self, trigger_type: str):
        super().__init__("domain.postback.trigger_type.invalid", {"trigger_type": trigger_type}, 400)


class InvalidPostbackEventKey(PostbackRuleException):
    def __init__(self):
        super().__init__("domain.postback.event_key.invalid", {}, 400)


class InvalidPostbackTemplateValue(PostbackRuleException):
    def __init__(self, value: str):
        super().__init__("domain.postback.template.value.invalid", {"value": value}, 400)
