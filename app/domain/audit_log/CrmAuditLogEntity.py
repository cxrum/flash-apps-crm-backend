from copy import deepcopy
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime
from typing import Any

_MISSING = object()
_NO_CHANGE = object()


@dataclass(frozen=True)
class CrmAuditLogEntity:
    entity_changed: str
    user_id: int | None = None
    app_id: int | None = None
    entity_id: str | None = None
    old_value: dict[str, Any] | list[Any] | None = None
    new_value: dict[str, Any] | list[Any] | None = None
    changed_at: datetime | None = None
    audit_log_id: int | None = None

    @classmethod
    def __recursive_diff(
        cls,
        old: Any,
        new: Any,
        ignored_fields: frozenset[str],
    ) -> Any:
        if old is _MISSING and new is _MISSING:
            return _NO_CHANGE
        if old is _MISSING:
            return deepcopy(new)
        if new is _MISSING:
            return None

        if isinstance(old, dict) and isinstance(new, dict):
            diff: dict[str, Any] = {}
            keys = list(old.keys())
            keys.extend(key for key in new.keys() if key not in old)

            for key in keys:
                if str(key) in ignored_fields:
                    continue

                changed_value = cls.__recursive_diff(
                    old.get(key, _MISSING),
                    new.get(key, _MISSING),
                    ignored_fields,
                )
                if changed_value is not _NO_CHANGE:
                    diff[key] = changed_value

            return diff if diff else _NO_CHANGE

        if old != new:
            return deepcopy(new)

        return _NO_CHANGE

    @staticmethod
    def __normalize_fragment(fragment: Any) -> dict[str, Any] | list[Any] | None:
        if fragment is _NO_CHANGE:
            return None
        if fragment is None or isinstance(fragment, dict | list):
            return fragment
        return {"value": fragment}

    @classmethod
    def create_from_diff(
        cls,
        old_value: dict[str, Any] | list[Any],
        new_value: dict[str, Any] | list[Any],
        *,
        user_id: int | None = None,
        app_id: int | None = None,
        entity_changed: str | None = None,
        entity_id: str | int | None = None,
        changed_at: datetime | None = None,
        ignore_fields: Sequence[str] | None = None,
    ) -> list["CrmAuditLogEntity"]:
        ignored_fields = frozenset(ignore_fields or ())

        if entity_changed is not None:
            new_diff = cls.__recursive_diff(old_value, new_value, ignored_fields)
            if new_diff is _NO_CHANGE:
                return []

            old_diff = cls.__recursive_diff(new_value, old_value, ignored_fields)
            return [
                cls(
                    entity_changed=entity_changed,
                    user_id=user_id,
                    app_id=app_id,
                    entity_id=None if entity_id is None else str(entity_id),
                    old_value=cls.__normalize_fragment(old_diff),
                    new_value=cls.__normalize_fragment(new_diff),
                    changed_at=changed_at,
                )
            ]

        if not isinstance(old_value, dict) or not isinstance(new_value, dict):
            raise ValueError("entity_changed is required when diffing non-dict audit values")

        audit_logs: list[CrmAuditLogEntity] = []
        keys = list(old_value.keys())
        keys.extend(key for key in new_value.keys() if key not in old_value)

        for key in keys:
            if str(key) in ignored_fields:
                continue

            old_entity_value = old_value.get(key, _MISSING)
            new_entity_value = new_value.get(key, _MISSING)
            new_diff = cls.__recursive_diff(old_entity_value, new_entity_value, ignored_fields)

            if new_diff is _NO_CHANGE:
                continue

            old_diff = cls.__recursive_diff(new_entity_value, old_entity_value, ignored_fields)
            audit_logs.append(
                cls(
                    entity_changed=str(key),
                    user_id=user_id,
                    app_id=app_id,
                    entity_id=None if entity_id is None else str(entity_id),
                    old_value=cls.__normalize_fragment(old_diff),
                    new_value=cls.__normalize_fragment(new_diff),
                    changed_at=changed_at,
                )
            )

        return audit_logs
