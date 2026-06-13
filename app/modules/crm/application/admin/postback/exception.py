from typing import Any, Dict

from app.modules.crm.application.admin.exception import AdminException


class PostbackExceptions(AdminException):
    def __init__(self, message_key: str = "internal", context: Dict[str, Any] = {}, code: int = 500):
        super().__init__(message_key, context, code)


class PostbackNotFound(PostbackExceptions):
    def __init__(self, postback_id: int | None = None):
        context = {"postback_id": postback_id} if postback_id is not None else {}
        super().__init__("admin.postback.not_found", context, 404)


class TemplateNotFound(PostbackExceptions):
    def __init__(self, template_code: str | None = None):
        context = {"template_code": template_code} if template_code is not None else {}
        super().__init__("admin.postback.template.not_found", context, 404)


class SecretNotFound(PostbackExceptions):
    def __init__(self, template_code: str | None = None):
        context = {"template_code": template_code} if template_code is not None else {}
        super().__init__("admin.postback.secret.not_found", context, 404)


class RuleNotFound(PostbackExceptions):
    def __init__(self, rule_id: int | None = None):
        context = {"rule_id": rule_id} if rule_id is not None else {}
        super().__init__("admin.postback.rule.not_found", context, 404)


class PostbackPlatformNotFound(PostbackExceptions):
    def __init__(self):
        super().__init__("admin.postback.platform.not_found", {}, 404)


class PostbackAppMismatch(PostbackExceptions):
    def __init__(self, app_id: int):
        super().__init__("admin.postback.app.mismatch", {"app_id": app_id}, 404)
