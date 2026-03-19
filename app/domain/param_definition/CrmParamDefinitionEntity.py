from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any

from app.domain.exceptions import DomainError


@dataclass(frozen=True)
class CrmParamDefinitionEntity:
    display_name: str
    machine_key: str
    data_type: str
    app_id: int | None = None
    description: str | None = None
    overwrite_policy: str = "replace"
    is_active: bool = True
    visible_in_logs: bool = True
    visible_in_stats: bool = False
    filterable: bool = False
    groupable: bool = False
    param_definition_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    
    @staticmethod
    def get_params_for_aggeregation(*, params: dict[str, Any], params_dictionary: list[CrmParamDefinitionEntity]) ->dict[str, Any]:
        filtered_params = {}
        
        for definiton in params_dictionary:
            if not definiton.groupable:
                continue
            
            value = definiton.get_param_value(params)

            if value is None:
                continue

            filtered_params[definiton.machine_key] = value
        
        return filtered_params
        
    def get_param_value(self, params: dict[str, Any]) -> object | None:
        if self.machine_key not in params:
            return None

        value = params[self.machine_key]
        if value is None:
            return None

        if self.data_type == "string":
            return str(value)
        if self.data_type == "integer":
            return self._coerce_integer(value)
        if self.data_type == "float":
            return self._coerce_float(value)
        if self.data_type == "boolean":
            return self._coerce_boolean(value)
        if self.data_type == "date":
            return self._coerce_date(value)
        if self.data_type == "datetime":
            return self._coerce_datetime(value)
        if self.data_type == "enum":
            return str(value)
        if self.data_type == "json":
            return self._coerce_json(value)
        if self.data_type == "list":
            return self._coerce_list(value)

        raise DomainError(f"Unsupported param data_type: {self.data_type}")

    def _coerce_integer(self, value: object) -> int:
        if isinstance(value, bool):
            raise self._invalid_value(value)
        if isinstance(value, int):
            return value
        if isinstance(value, float):
            if value.is_integer():
                return int(value)
            raise self._invalid_value(value)
        if isinstance(value, str):
            stripped = value.strip()
            if not stripped:
                raise self._invalid_value(value)
            try:
                return int(stripped)
            except ValueError as error:
                raise self._invalid_value(value) from error
        raise self._invalid_value(value)

    def _coerce_float(self, value: object) -> float:
        if isinstance(value, bool):
            raise self._invalid_value(value)
        if isinstance(value, int | float):
            return float(value)
        if isinstance(value, str):
            stripped = value.strip()
            if not stripped:
                raise self._invalid_value(value)
            try:
                return float(stripped)
            except ValueError as error:
                raise self._invalid_value(value) from error
        raise self._invalid_value(value)

    def _coerce_boolean(self, value: object) -> bool:
        if isinstance(value, bool):
            return value
        if isinstance(value, int):
            if value in (0, 1):
                return bool(value)
            raise self._invalid_value(value)
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in {"1", "true", "t", "yes", "y", "on"}:
                return True
            if normalized in {"0", "false", "f", "no", "n", "off"}:
                return False
        raise self._invalid_value(value)

    def _coerce_date(self, value: object) -> date:
        if isinstance(value, datetime):
            return value.date()
        if isinstance(value, date):
            return value
        if isinstance(value, str):
            stripped = value.strip()
            if not stripped:
                raise self._invalid_value(value)
            try:
                return date.fromisoformat(stripped)
            except ValueError as error:
                raise self._invalid_value(value) from error
        raise self._invalid_value(value)

    def _coerce_datetime(self, value: object) -> datetime:
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            stripped = value.strip()
            if not stripped:
                raise self._invalid_value(value)
            normalized = stripped.replace("Z", "+00:00")
            try:
                return datetime.fromisoformat(normalized)
            except ValueError as error:
                raise self._invalid_value(value) from error
        raise self._invalid_value(value)

    def _coerce_json(self, value: object) -> object:
        if isinstance(value, str):
            stripped = value.strip()
            if not stripped:
                raise self._invalid_value(value)
            try:
                return json.loads(stripped)
            except json.JSONDecodeError as error:
                raise self._invalid_value(value) from error
        return value

    def _coerce_list(self, value: object) -> list[object]:
        if isinstance(value, list):
            return list(value)
        if isinstance(value, tuple | set):
            return list(value)
        if isinstance(value, str):
            stripped = value.strip()
            if not stripped:
                return []
            try:
                parsed = json.loads(stripped)
            except json.JSONDecodeError:
                return [
                    item.strip()
                    for item in stripped.split(",")
                    if item.strip()
                ]
            if isinstance(parsed, list):
                return parsed
            raise self._invalid_value(value)
        raise self._invalid_value(value)

    def _invalid_value(self, value: object) -> DomainError:
        return DomainError(
            f"Param '{self.machine_key}' expected {self.data_type}, got {value!r}",
        )
