from typing import Any, Dict

from app.application.admin.exception import AdminException


class SecretsException(AdminException):
    def __init__(self, message_key: str = "internal", context: Dict[str, Any]={}, code: int = 500):
        super().__init__(message_key, context, code)


class SecretTemplateNotFound(SecretsException):
    def __init__(self, template_id: int | None = None):
        context = {"template_id": template_id} if template_id is not None else {}
        super().__init__("admin.secret.template.not_found", context, 404)


class AppSecretNotFound(SecretsException):
    def __init__(self, secret_id: int | None = None):
        context = {"secret_id": secret_id} if secret_id is not None else {}
        super().__init__("admin.secret.app_secret.not_found", context, 404)
