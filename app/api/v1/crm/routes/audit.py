from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query

from app.api.v1.crm.payloads import AuditLogQueryPayload
from app.api.v1.transport import PaginationQueryPayload
from app.application.admin.logs.mappers import LogsResponseMapper
from app.application.admin.logs.protocol import LogsServiceProtocol
from app.application.base import JsonDict
from app.application.crm_authentication.responses import ResolvedCrmUserResponse
from app.core.utils.general_mapper import GeneralMapper
from app.di.dependencies import resolve_user
from app.di.services import get_admin_logs_service

router = APIRouter()


@router.get("/", tags=["admin", "audit"])
async def get_audit_logs(
    pagination_queries: Annotated[PaginationQueryPayload, Query()],
    audit_queries: Annotated[AuditLogQueryPayload, Query()],
    crm_user: ResolvedCrmUserResponse = Depends(resolve_user),
    logs_service: LogsServiceProtocol = Depends(get_admin_logs_service),
) -> JsonDict:
    command = LogsResponseMapper.audit_logs_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, audit_queries, pagination_queries)
    )
    response = logs_service.list_audit_logs(command)
    return response.model_dump(mode="json")
