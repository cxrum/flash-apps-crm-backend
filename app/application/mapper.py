from typing import TypeVar


from app.application.base import PaginationCommand
from app.domain.pagination import Pagination

class PaginationMapper:
        
    @staticmethod
    def pagination_from_command(command: PaginationCommand) -> Pagination:
        # TODO Make start_at and end_at with static variable checking. Dont use getattr method.
        return Pagination(
            start_at=getattr(command, "start_at", None),
            end_at=getattr(command, "end_at", None),
            limit=command.limit,
            offset=command.offset,
        )