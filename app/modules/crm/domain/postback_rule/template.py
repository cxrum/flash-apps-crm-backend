from __future__ import annotations

import re
from collections.abc import ItemsView, Iterator, KeysView, Mapping, ValuesView
from dataclasses import dataclass, field
from typing import Any

from app.modules.crm.domain.postback_rule.exception import InvalidPostbackTemplateValue


@dataclass
class PostbackTemplateEntity:
    _template: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self._template = dict(self._template)
        self.validate_payload()

    def validate_payload(self):
        for _, value in self._template.items():
            if not self.validate_value_key(value):
                raise InvalidPostbackTemplateValue(value)

    def set_payload(self, new: dict[str, str]):
        candidate_template: dict[str, str] = {}

        for key, value in new.items():
            if self.validate_value_key(value):
                candidate_template[key] = value
            else:
                raise InvalidPostbackTemplateValue(value)

        self._template = candidate_template

    @staticmethod
    def from_dict(value: dict[str, str]) -> "PostbackTemplateEntity":
        entity = PostbackTemplateEntity()
        entity.set_payload(value)
        return entity

    @staticmethod
    def _get_param_value_types() -> list[str]:
        return ["current", "snapshot"]

    @staticmethod
    def validate_value_key(value_key: str) -> bool:
        match = re.fullmatch(r"\{(\S+)\}", value_key)

        if match is None:
            return False

        _t = match[1].split(".")

        if len(_t) == 2:
            if _t[0] not in PostbackTemplateEntity._get_param_value_types():
                return False

        return match is not None

    @staticmethod
    def _normalize_value(value: str) -> str:
        return value[1:-1] if value.startswith("{") and value.endswith("}") else value

    def normalized(self) -> dict[str, str]:
        res = {}

        for key, value in self._template.items():
            res[key] = self._normalize_value(value)

        return res

    def set_value(self, key: str, value_key: str):
        if not self.validate_value_key(value_key):
            raise InvalidPostbackTemplateValue(value_key)

        self._template[key] = value_key

    def __getitem__(self, key: str) -> str:
        return self._template[key]

    def __setitem__(self, key: str, value: str) -> None:
        self.set_value(key, value)

    def __delitem__(self, key: str) -> None:
        del self._template[key]

    def __contains__(self, key: object) -> bool:
        return key in self._template

    def __iter__(self) -> Iterator[str]:
        return iter(self._template)

    def __len__(self) -> int:
        return len(self._template)

    def get(self, key: str, default: str | None = None) -> str | None:
        return self._template.get(key, default)

    def keys(self) -> KeysView[str]:
        return self._template.keys()

    def values(self) -> ValuesView[str]:
        return self._template.values()

    def items(self) -> ItemsView[str, str]:
        return self._template.items()

    def update(
        self,
        other: Mapping[str, str] | None = None,
        **kwargs: str,
    ) -> None:
        updates = dict(other or {})
        updates.update(kwargs)

        for key, value in updates.items():
            self.set_value(key, value)

    def pop(self, key: str, default: Any = ...) -> str:
        if default is ...:
            return self._template.pop(key)
        return self._template.pop(key, default)

    def clear(self) -> None:
        self._template.clear()
