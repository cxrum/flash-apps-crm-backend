from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query

from app.modules.crm.api.v1.crm.payloads import AuditLogQueryPayload
from app.modules.crm.api.v1.transport import PaginationQueryPayload
from app.modules.crm.application.admin.audit.mappers import AuditResponseMapper
from app.modules.crm.application.admin.audit.protocol import AuditServiceProtocol
from app.modules.crm.application.base import JsonDict
from app.modules.crm.application.crm_authentication.responses import ResolvedCrmUserResponse
from app.modules.crm.core.utils.general_mapper import GeneralMapper
from app.modules.crm.di.dependencies import resolve_user
from app.modules.crm.di.services import get_admin_audit_service

router = APIRouter()


@router.get("/", tags=["admin", "audit"])
async def get_audit_logs(
    pagination_queries: Annotated[PaginationQueryPayload, Query()],
    audit_queries: Annotated[AuditLogQueryPayload, Query()],
    crm_user: Annotated[ResolvedCrmUserResponse, Depends(resolve_user)],
    audit_service: Annotated[AuditServiceProtocol, Depends(get_admin_audit_service)],
) -> JsonDict:
    command = AuditResponseMapper.audit_logs_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, audit_queries, pagination_queries)
    )
    response = audit_service.list_audit_logs(command)
    return response.model_dump(mode="json")
