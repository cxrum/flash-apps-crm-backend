from dataclasses import dataclass


@dataclass(frozen=True)
class Pagination:
    start_at: str | None = None
    end_at: str | None = None
    limit: int | None = None
    offset: int | None = None