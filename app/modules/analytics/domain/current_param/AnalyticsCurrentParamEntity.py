from copy import deepcopy
from dataclasses import dataclass
from datetime import UTC, date, datetime
from decimal import Decimal
from typing import Any, ClassVar, Protocol

from app.modules.analytics.domain.current_param.exception import (
    AppendPolicyNotSupported,
    MergePolicyNotSupported,
    UnsupportedCurrentParamUpdatePolicy,
)


class CurrentParamUpdateStrategyProtocol(Protocol):
    def apply(self, current_value: Any | None, incoming_value: Any) -> Any | None: ...


class _ReplaceCurrentParamStrategy:
    def apply(self, current_value: Any | None, incoming_value: Any) -> Any | None:
        return incoming_value


class _AppendCurrentParamStrategy:
    def apply(self, current_value: Any | None, incoming_value: Any) -> Any | None:
        if current_value is None:
            return incoming_value
        if isinstance(current_value, list):
            values = list(current_value) + (list(incoming_value) if isinstance(incoming_value, list) else [incoming_value])
            return list(dict.fromkeys(values))
        if isinstance(current_value, str) and isinstance(incoming_value, str):
            return current_value + incoming_value
        if isinstance(current_value, int | float) and isinstance(incoming_value, int | float):
            return current_value + incoming_value
        raise AppendPolicyNotSupported()


class _MergeCurrentParamStrategy:
    def apply(self, current_value: Any | None, incoming_value: Any) -> Any | None:
        if current_value is None:
            return incoming_value
        if isinstance(current_value, dict) and isinstance(incoming_value, dict):
            return {**deepcopy(current_value), **deepcopy(incoming_value)}
        if isinstance(current_value, list):
            values = list(current_value) + (list(incoming_value) if isinstance(incoming_value, list) else [incoming_value])
            return list(dict.fromkeys(values))
        raise MergePolicyNotSupported()


@dataclass
class AnalyticsCurrentParamEntity:
    click_id: str
    param_key: str
    value_string: str | None = None
    value_number: float | None = None
    value_bool: bool | None = None
    value_json: dict[str, Any] | list[Any] | None = None
    updated_at: datetime | None = None

    _UPDATE_STRATEGIES: ClassVar[dict[str, CurrentParamUpdateStrategyProtocol]] = {
        "replace": _ReplaceCurrentParamStrategy(),
        "append": _AppendCurrentParamStrategy(),
        "merge": _MergeCurrentParamStrategy(),
    }

    def current_value(self) -> Any | None:
        if self.value_json is not None:
            return deepcopy(self.value_json)
        if self.value_bool is not None:
            return self.value_bool
        if self.value_number is not None:
            return self.value_number
        return self.value_string

    def update_param(self, update_policy: str, value: Any) -> None:
        strategy = self._UPDATE_STRATEGIES.get(update_policy)
        if strategy is None:
            raise UnsupportedCurrentParamUpdatePolicy(update_policy)
        self._assign_value(strategy.apply(self.current_value(), self._normalize_value(value)))
        self.updated_at = datetime.now(tz=UTC)

    def _assign_value(self, value: Any) -> None:
        self.value_string = self.value_number = self.value_bool = self.value_json = None
        if value is None:
            return
        if isinstance(value, bool):
            self.value_bool = value
        elif isinstance(value, int | float | Decimal):
            self.value_number = float(value)
        elif isinstance(value, dict | list):
            self.value_json = deepcopy(value)
        elif isinstance(value, datetime):
            self.value_string = (value.astimezone(UTC) if value.tzinfo else value.replace(tzinfo=UTC)).isoformat()
        elif isinstance(value, date):
            self.value_string = value.isoformat()
        else:
            self.value_string = str(value)

    @staticmethod
    def _normalize_value(value: Any) -> Any | None:
        if value is None:
            return None
        if isinstance(value, datetime):
            return (value.astimezone(UTC) if value.tzinfo else value.replace(tzinfo=UTC)).isoformat()
        if isinstance(value, date):
            return value.isoformat()
        if isinstance(value, tuple | set):
            return list(value)
        return deepcopy(value) if isinstance(value, dict | list) else value
