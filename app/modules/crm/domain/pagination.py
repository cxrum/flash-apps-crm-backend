from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Pagination:
    start_at: datetime | None = None
    end_at: datetime | None = None
    limit: int | None = None
    offset: int | None = None