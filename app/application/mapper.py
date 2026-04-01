from datetime import UTC
from typing import TypeVar


from app.api.v1.transport import PaginationQueryPayload
from app.application.base import PaginationCommand
from app.domain.pagination import Pagination

class PaginationMapper:
        
    @classmethod
    def pagination_from_command(cls, command: PaginationCommand) -> Pagination:
        return Pagination(
            start_at=command.start_at.astimezone(UTC) if command.start_at is not None else None,
            end_at=command.end_at.astimezone(UTC) if command.end_at is not None else None,
            limit=command.limit,
            offset=command.offset,
        )
        