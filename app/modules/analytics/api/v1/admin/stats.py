from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.modules.analytics.application.admin.logs.protocol import AnalyticsLogsServiceProtocol
from app.modules.analytics.di.services import get_analytics_logs_service
from app.modules.crm.api.v1.crm.payloads import ClickLogsQueryPayload, EventLogsQueryPayload, StatsQueryPayload
from app.modules.crm.api.v1.stubs import build_stub_response
from app.modules.crm.api.v1.transport import PaginationQueryPayload
from app.modules.crm.application.admin.logs.mappers import LogsResponseMapper
from app.modules.crm.application.base import JsonDict
from app.modules.crm.application.crm_authentication.responses import ResolvedCrmUserResponse
from app.modules.crm.core.utils.general_mapper import GeneralMapper
from app.modules.crm.di.dependencies import resolve_user

router = APIRouter()


@router.get("/", tags=["admin", "stats"])
async def get_stats(
    pagination_queries: Annotated[PaginationQueryPayload, Query()],
    stats_queries: Annotated[StatsQueryPayload, Query()],
    crm_user: ResolvedCrmUserResponse = Depends(resolve_user),
) -> JsonDict:
    command = LogsResponseMapper.audit_logs_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, stats_queries, pagination_queries)
    )
    return build_stub_response(command)  # type: ignore


@router.get("/logs/clicks", tags=["admin", "stats"])
async def list_click_logs(
    pagination_queries: Annotated[PaginationQueryPayload, Query()],
    click_log_queries: Annotated[ClickLogsQueryPayload, Query()],
    crm_user: ResolvedCrmUserResponse = Depends(resolve_user),
    logs_service: AnalyticsLogsServiceProtocol = Depends(get_analytics_logs_service),
) -> JsonDict:
    command = LogsResponseMapper.click_logs_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, click_log_queries, pagination_queries)
    )
    response = logs_service.list_clicks(command)
    return response.model_dump(mode="json")


@router.get("/logs/events", tags=["admin", "stats"])
async def list_event_logs(
    pagination_queries: Annotated[PaginationQueryPayload, Query()],
    event_log_queries: Annotated[EventLogsQueryPayload, Query()],
    crm_user: ResolvedCrmUserResponse = Depends(resolve_user),
    logs_service: AnalyticsLogsServiceProtocol = Depends(get_analytics_logs_service),
) -> JsonDict:
    command = LogsResponseMapper.event_logs_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, event_log_queries, pagination_queries)
    )
    response = logs_service.list_raw_events(command)
    return response.model_dump(mode="json")
