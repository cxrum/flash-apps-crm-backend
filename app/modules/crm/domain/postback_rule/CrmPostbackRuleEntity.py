from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from urllib.parse import urlparse

from app.modules.crm.domain.postback_rule.exception import (
    InvalidPostbackEventKey,
    InvalidPostbackHttpMethod,
    InvalidPostbackTriggerType,
    InvalidPostbackUrlScheme,
    MissingPostbackUrlHost,
    MissingSecretTemplate,
    PostbackUrlContainsSpaces,
    PostbackUrlRequired,
)
from app.modules.crm.domain.postback_rule.template import PostbackTemplateEntity


@dataclass
class CrmPostbackRuleEntity:
    platform_app_id: int
    name: str
    endpoint_url: str
    trigger_type: str
    http_method: str = "POST"
    headers: dict[str, Any] = field(default_factory=dict)
    auth_params: dict[str, str] = field(default_factory=dict)  # Structure {outer_auth_key: inner_secret_template_key}
    timeout: int = 0
    event_key: str | None = None
    template: PostbackTemplateEntity = field(default_factory=PostbackTemplateEntity)
    retry_policy: dict[str, Any] = field(default_factory=dict)
    is_active: bool = True
    rule_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def validate_http_method(self):
        if self.http_method not in ["POST", "GET"]:
            raise InvalidPostbackHttpMethod(self.http_method)

    def validate_secrets(self, secrets_codes: list[str]):
        for _, value in self.auth_params.items():
            if value not in secrets_codes:
                raise MissingSecretTemplate(value)

    def validate_url(self):
        if not self.endpoint_url or not self.endpoint_url.strip():
            raise PostbackUrlRequired()

        if self.endpoint_url != self.endpoint_url.strip() or any(char.isspace() for char in self.endpoint_url):
            raise PostbackUrlContainsSpaces()

        parsed_url = urlparse(self.endpoint_url)

        if parsed_url.scheme not in {"http", "https"}:
            raise InvalidPostbackUrlScheme()

        if not parsed_url.netloc or parsed_url.hostname is None:
            raise MissingPostbackUrlHost()

    def validate_event_key(self):
        if self.trigger_type not in ["install", "param_update", "metric", "conversion"]:
            raise InvalidPostbackTriggerType(self.trigger_type)

        if self.trigger_type not in ["metric", "conversion"] and self.event_key is not None:
            raise InvalidPostbackEventKey()

    def update(
        self,
        *,
        platform_app_id: int | None = None,
        name: str | None = None,
        endpoint_url: str | None = None,
        trigger_type: str | None = None,
        http_method: str | None = None,
        headers: dict[str, Any] | None = None,
        auth_params: dict[str, str] | None = None,
        timeout: int | None = None,
        event_key: str | None = None,
        template: PostbackTemplateEntity | None = None,
        retry_policy: dict[str, Any] | None = None,
        is_active: bool | None = None,
    ) -> None:
        self.platform_app_id = platform_app_id if platform_app_id is not None else self.platform_app_id
        self.name = name if name is not None else self.name
        self.endpoint_url = endpoint_url if endpoint_url is not None else self.endpoint_url
        self.trigger_type = trigger_type if trigger_type is not None else self.trigger_type
        self.http_method = http_method if http_method is not None else self.http_method
        self.headers = headers if headers is not None else self.headers
        self.auth_params = auth_params if auth_params is not None else self.auth_params
        self.timeout = timeout if timeout is not None else self.timeout
        self.event_key = event_key if event_key is not None else self.event_key
        self.template = template if template is not None else self.template
        self.retry_policy = retry_policy if retry_policy is not None else self.retry_policy
        self.is_active = is_active if is_active is not None else self.is_active

        if event_key is not None:
            self.event_key = event_key
        elif trigger_type is not None and trigger_type not in ["metric", "conversion"]:
            self.event_key = None

        self.updated_at = datetime.now(UTC)
