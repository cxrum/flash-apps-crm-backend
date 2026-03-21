from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from urllib.parse import urlparse

from app.domain.exceptions import DomainError
from app.domain.postback_rule.template import PostbackTemplateEntity


@dataclass()
class CrmPostbackRuleEntity:
    platfrom_app_id: int
    name: str
    endpoint_url: str
    trigger_type: str
    http_method: str = "POST"
    headers: dict[str, Any] = field(default_factory=dict)
    auth_params: dict[str, str] = field(default_factory=dict) # Structure {outer_auth_key: inner_secret_template_key}
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
            raise DomainError()    
        
    def validate_secrets(self, secrets_codes: list[str]):
        for _, value in self.auth_params.items():
            if value not in secrets_codes:
                raise DomainError(f"Secret template: {value} doesnt exsit")
    
    def validate_url(self):
        if not self.endpoint_url or not self.endpoint_url.strip():
            raise DomainError("Postback endpoint URL is required")

        if self.endpoint_url != self.endpoint_url.strip() or any(
            char.isspace() for char in self.endpoint_url
        ):
            raise DomainError("Postback endpoint URL must not contain spaces")

        parsed_url = urlparse(self.endpoint_url)

        if parsed_url.scheme not in {"http", "https"}:
            raise DomainError("Postback endpoint URL must use http or https")

        if not parsed_url.netloc or parsed_url.hostname is None:
            raise DomainError("Postback endpoint URL must include a host")
    
    def validate_event_key(self):
        if self.trigger_type not in ["install", "param_update", "metric", "conversion"]:
            raise DomainError()
        
        if self.trigger_type not in ["metric", "conversion"] and self.event_key is not None:
            raise DomainError()