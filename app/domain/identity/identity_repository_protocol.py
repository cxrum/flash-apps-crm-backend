from __future__ import annotations

from datetime import datetime
from typing import Protocol


class IdentityRepositoryProtocol(Protocol):
    def upsert_user(self, user_id: str) -> None: ...
    def upsert_identity(self, *, anonymous_id: str, user_id: str, linked_at: datetime) -> None: ...
    def upsert_identities(self, identity_links: dict[str, str | None]) -> None: ...
