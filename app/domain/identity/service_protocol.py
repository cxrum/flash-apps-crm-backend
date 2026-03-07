from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol


@dataclass
class IdentityLinkResult:
    status: str
    anonymous_id: str
    user_id: str
    linked_at: datetime

    def as_dict(self) -> dict[str, str]:
        return {
            "status": self.status,
            "anonymous_id": self.anonymous_id,
            "user_id": self.user_id,
            "linked_at": self.linked_at.isoformat(),
        }


class IdentityServiceProtocol(Protocol):
    def link_identity(self, *, anonymous_id: str, user_id: str, linked_at: datetime) -> IdentityLinkResult: ...

