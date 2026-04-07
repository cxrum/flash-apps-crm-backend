from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query

from app.api.v1.crm.payloads import ClickLogsQueryPayload, EventLogsQueryPayload, StatsQueryPayload
from app.api.v1.stubs import build_stub_response
from app.api.v1.transport import PaginationQueryPayload
from app.application.admin.logs.mappers import LogsResponseMapper
from app.application.admin.logs.service import LogsService
from app.application.crm_authentication.responses import ResolvedCrmUserResponse
from app.core.utils.general_mapper import GeneralMapper
from app.di.dependencies import resolve_user
from app.di.services import get_admin_logs_service

router = APIRouter()


@router.get("/", tags=["admin", "stats"])
async def get_stats(
    pagination_queries: Annotated[PaginationQueryPayload, Query()],
    stats_queries: Annotated[StatsQueryPayload, Query()],
    crm_user: ResolvedCrmUserResponse = Depends(resolve_user),
) -> str:
    command = LogsResponseMapper.audit_logs_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, stats_queries, pagination_queries)
    )
    return build_stub_response(command)


@router.get("/logs/clicks", tags=["admin", "stats"])
async def list_click_logs(
    pagination_queries: Annotated[PaginationQueryPayload, Query()],
    click_log_queries: Annotated[ClickLogsQueryPayload, Query()],
    crm_user: ResolvedCrmUserResponse = Depends(resolve_user),
    logs_service: LogsService = Depends(get_admin_logs_service),
) -> str:
    command = LogsResponseMapper.click_logs_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, click_log_queries, pagination_queries)
    )
    response = logs_service.list_clicks(command)
    return response.model_dump_json()


@router.get("/logs/events", tags=["admin", "stats"])
async def list_event_logs(
    pagination_queries: Annotated[PaginationQueryPayload, Query()],
    event_log_queries: Annotated[EventLogsQueryPayload, Query()],
    crm_user: ResolvedCrmUserResponse = Depends(resolve_user),
    logs_service: LogsService = Depends(get_admin_logs_service),
) -> str:
    command = LogsResponseMapper.event_logs_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, event_log_queries, pagination_queries)
    )
    response = logs_service.list_raw_events(command)
    return response.model_dump_json()
