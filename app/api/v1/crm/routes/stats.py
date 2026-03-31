from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query

from app.api.v1.crm.payloads import ClickLogsQueryPayload, EventLogsQueryPayload, StatsQueryPayload
from app.api.v1.stubs import build_stub_response
from app.api.v1.transport import PaginationQueryPayload
from app.application.admin.logs.mappers import LogsResponseMapper
from app.application.crm_authentication.entities import ResolvedCrmUser
from app.core.utils.general_mapper import GeneralMapper
from app.di.dependencies import resolve_user

router = APIRouter()


@router.get("/", tags=["admin", "stats"])
async def get_stats(
    pagination_queries: Annotated[PaginationQueryPayload, Query()],
    stats_queries: Annotated[StatsQueryPayload, Query()],
    crm_user: ResolvedCrmUser = Depends(resolve_user),
) -> dict[str, Any]:
    command = LogsResponseMapper.audit_logs_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, stats_queries, pagination_queries)
    )
    return build_stub_response(command)


@router.get("/logs/clicks", tags=["admin", "stats"])
async def list_click_logs(
    pagination_queries: Annotated[PaginationQueryPayload, Query()],
    click_log_queries: Annotated[ClickLogsQueryPayload, Query()],
    crm_user: ResolvedCrmUser = Depends(resolve_user),
) -> dict[str, Any]:
    command = LogsResponseMapper.click_logs_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, click_log_queries, pagination_queries)
    )
    return build_stub_response(command)


@router.get("/logs/events", tags=["admin", "stats"])
async def list_event_logs(
    pagination_queries: Annotated[PaginationQueryPayload, Query()],
    event_log_queries: Annotated[EventLogsQueryPayload, Query()],
    crm_user: ResolvedCrmUser = Depends(resolve_user),
) -> dict[str, Any]:
    command = LogsResponseMapper.event_logs_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, event_log_queries, pagination_queries)
    )
    return build_stub_response(command)
