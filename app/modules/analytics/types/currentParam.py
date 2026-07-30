from copy import deepcopy
from dataclasses import dataclass
from datetime import UTC, date, datetime
from decimal import Decimal
from typing import Any, ClassVar, Protocol

from app.modules.analytics.domain.current_param.exception import UnsupportedCurrentParamUpdatePolicy
from app.modules.crm.domain.param_definition.CrmParamDefinitionEntity import CrmParamDefinitionEntity


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
            appended = list(current_value)
            if isinstance(incoming_value, list):
                appended.extend(incoming_value)
            else:
                appended.append(incoming_value)

            _temp = []
            for val in appended:
                if val not in _temp:
                    _temp.append(val)

            return _temp

        if isinstance(current_value, str) and isinstance(incoming_value, str):
            return current_value + incoming_value

        if isinstance(current_value, int | float) and isinstance(incoming_value, int | float):
            return current_value + incoming_value


class _MergeCurrentParamStrategy:
    def apply(self, current_value: Any | None, incoming_value: Any) -> Any | None:
        if current_value is None:
            return incoming_value

        if isinstance(current_value, dict) and isinstance(incoming_value, dict):
            return {
                **deepcopy(current_value),
                **deepcopy(incoming_value),
            }

        if isinstance(current_value, list):
            merged = list(current_value)
            incoming_items = incoming_value if isinstance(incoming_value, list) else [incoming_value]
            for item in incoming_items:
                if item not in merged:
                    merged.append(item)
            return merged


@dataclass
class CurrentParam:
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

        normalized_value = self._normalize_value(value)
        new_value = strategy.apply(self.current_value(), normalized_value)
        self._assign_value(new_value)
        self.updated_at = datetime.now(tz=UTC)

    def _assign_value(self, value: Any | None) -> None:
        self.value_string = None
        self.value_number = None
        self.value_bool = None
        self.value_json = None

        if value is None:
            return

        if isinstance(value, bool):
            self.value_bool = value
            return

        if isinstance(value, int | float | Decimal):
            self.value_number = float(value)
            return

        if isinstance(value, dict):
            self.value_json = deepcopy(value)
            return

        if isinstance(value, list):
            self.value_json = deepcopy(value)
            return

        self.value_string = str(value)

    def _normalize_value(self, value: Any) -> Any | None:
        if value is None:
            return None

        if isinstance(value, datetime):
            normalized = value.astimezone(UTC) if value.tzinfo is not None else value.replace(tzinfo=UTC)
            return normalized.isoformat()

        if isinstance(value, date):
            return value.isoformat()

        if isinstance(value, tuple | set):
            return list(value)

        if isinstance(value, dict):
            return deepcopy(value)

        if isinstance(value, list):
            return list(value)

        return value
