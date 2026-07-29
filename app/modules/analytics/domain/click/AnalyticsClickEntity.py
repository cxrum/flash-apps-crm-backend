from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from app.modules.crm.domain.param_definition.CrmParamDefinitionEntity import CrmParamDefinitionEntity
from app.modules.analytics.domain.click.exception import AnalyticsClickPlatformMismatch, AnalyticsClickStatusInvalid


@dataclass
class AnalyticsClickEntity:
    click_id: str
    app_platform_id: int
    status: str = "accepted"
    raw_query: dict[str, Any] = field(default_factory=dict)
    ip_address: str | None = None
    user_agent: str | None = None
    country_code: str | None = None
    region: str | None = None
    city: str | None = None
    language: str | None = None
    referrer: str | None = None
    source: str | None = None
    redirect_target: str | None = None
    normalized_params: dict[str, Any] = field(default_factory=dict)
    created_at: datetime | None = None

    @classmethod
    def create_synthetic(cls, app_platform_id: int, params: dict[str, Any]) -> "AnalyticsClickEntity":
        return cls(
            click_id=cls.generate_click_id(),
            app_platform_id=app_platform_id,
            raw_query=params,
            source="sdk_install",
        )

    def normalize_params(self, definitions: list[CrmParamDefinitionEntity]) -> None:
        self.normalized_params = {
            definition.machine_key: definition.get_param_value(self.raw_query) for definition in definitions
        }

    @staticmethod
    def generate_click_id() -> str:
        return str(uuid.uuid4())

    def set_new_click_id(self) -> None:
        self.click_id = self.generate_click_id()

    def accepted(self) -> None:
        self.status = "accepted"

    def rejected(self) -> None:
        self.status = "rejected"

    def duplicate(self) -> None:
        self.status = "duplicate"

    def redirected(self) -> None:
        self.status = "redirected"

    def validate_click_status(self) -> None:
        if self.status not in {"accepted", "redirected", "duplicate", "rejected", "test"}:
            raise AnalyticsClickStatusInvalid()

    def validate_platform_match(self, expected_platform_id: int) -> None:
        if self.app_platform_id != expected_platform_id:
            raise AnalyticsClickPlatformMismatch()
