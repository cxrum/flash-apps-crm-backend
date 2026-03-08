
from __future__ import annotations


from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class AppEntity:
    app_id: int
    app_secret_hash: str
    created_at: datetime