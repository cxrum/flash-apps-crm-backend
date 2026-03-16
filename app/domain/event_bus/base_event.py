from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, TypeVar
import uuid



@dataclass(frozen=True, slots=True)
class DomainEventMessage:
    name: str
    correlation_id: str = field(default_factory=lambda: str(uuid.uuid1()))
    payload: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    occurred_at: datetime = field(default_factory=lambda: datetime.now(tz=UTC))


