from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query

from app.api.v1.crm.payloads import AuditLogQueryPayload
from app.api.v1.transport import PaginationQueryPayload
from app.application.admin.logs.mappers import LogsResponseMapper
from app.application.admin.logs.service import LogsService
from app.application.crm_authentication.entities import ResolvedCrmUser
from app.core.utils.general_mapper import GeneralMapper
from app.di.dependencies import get_admin_logs_service, resolve_user

router = APIRouter()


@router.get("/", tags=["admin", "audit"])
async def get_audit_logs(
    pagination_queries: Annotated[PaginationQueryPayload, Query()],
    audit_queries: Annotated[AuditLogQueryPayload, Query()],
    crm_user: ResolvedCrmUser = Depends(resolve_user),
    logs_service: LogsService = Depends(get_admin_logs_service),
) -> str:
    command = LogsResponseMapper.audit_logs_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, audit_queries, pagination_queries)
    )
    response = logs_service.list_audit_logs(command)
    return response.model_dump_json()
