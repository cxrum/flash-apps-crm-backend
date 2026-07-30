from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.infra.di import get_admin_ingestion_data_service
from app.modules.crm.api.v1.crm.payloads import ClickLogsQueryPayload, EventLogsQueryPayload, StatsQueryPayload
from app.modules.crm.api.v1.stubs import build_stub_response
from app.modules.crm.api.v1.transport import PaginationQueryPayload
from app.modules.crm.application.admin.audit.mappers import AuditResponseMapper
from app.modules.crm.application.admin.ingestion.mappers import IngestionDataResponseMapper
from app.modules.crm.application.admin.ingestion.protocol import IngestionDataServiceProtocol
from app.modules.crm.application.base import JsonDict
from app.modules.crm.application.crm_authentication.responses import ResolvedCrmUserResponse
from app.modules.crm.core.utils.general_mapper import GeneralMapper
from app.modules.crm.di.dependencies import resolve_user

router = APIRouter()


@router.get("/", tags=["admin", "stats"])
async def get_stats(
    pagination_queries: Annotated[PaginationQueryPayload, Query()],
    stats_queries: Annotated[StatsQueryPayload, Query()],
    crm_user: Annotated[ResolvedCrmUserResponse, Depends(resolve_user)],
) -> JsonDict:
    command = AuditResponseMapper.audit_logs_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, stats_queries, pagination_queries)
    )
    return build_stub_response(command)  # type: ignore


@router.get("/logs/clicks", tags=["admin", "stats"])
async def list_click_logs(
    pagination_queries: Annotated[PaginationQueryPayload, Query()],
    click_log_queries: Annotated[ClickLogsQueryPayload, Query()],
    crm_user: Annotated[ResolvedCrmUserResponse, Depends(resolve_user)],
    ingestion_service: Annotated[IngestionDataServiceProtocol, Depends(get_admin_ingestion_data_service)],
) -> JsonDict:
    command = IngestionDataResponseMapper.click_logs_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, click_log_queries, pagination_queries)
    )
    response = ingestion_service.list_clicks(command)
    return response.model_dump(mode="json")


@router.get("/logs/events", tags=["admin", "stats"])
async def list_event_logs(
    pagination_queries: Annotated[PaginationQueryPayload, Query()],
    event_log_queries: Annotated[EventLogsQueryPayload, Query()],
    crm_user: Annotated[ResolvedCrmUserResponse, Depends(resolve_user)],
    ingestion_service: Annotated[IngestionDataServiceProtocol, Depends(get_admin_ingestion_data_service)],
) -> JsonDict:
    command = IngestionDataResponseMapper.event_logs_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, event_log_queries, pagination_queries)
    )
    response = ingestion_service.list_raw_events(command)
    return response.model_dump(mode="json")
