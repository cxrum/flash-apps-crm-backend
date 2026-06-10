from typing import Annotated

from fastapi import APIRouter, Body, Depends, Query

from app.application.base import JsonDict
from app.core.utils.general_mapper import GeneralMapper
from app.api.v1.crm.payloads import AppScopeQueryPayload, RolesQueryPayload, ShareAppPayload
from app.api.v1.transport import PaginationQueryPayload
from app.application.admin.crm_authorization.mappers import AuthenticationResponseMapper as AdminCommandMapper
from app.application.admin.crm_authorization.protocol import CrmAuthorizationServiceProtocol
from app.application.crm_authentication.responses import ResolvedCrmUserResponse
from app.di.dependencies import resolve_user
from app.di.services import get_crm_authorization_service

router = APIRouter()


@router.get("/", tags=["admin", "roles"])
async def list_roles(
    pagination_queries: Annotated[PaginationQueryPayload, Query()],
    role_queries: Annotated[RolesQueryPayload, Query()],
    crm_user: ResolvedCrmUserResponse = Depends(resolve_user),
    authorization_service: CrmAuthorizationServiceProtocol = Depends(get_crm_authorization_service),
) -> JsonDict:
    command = AdminCommandMapper.list_roles_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, role_queries, pagination_queries)
    )
    response = authorization_service.list_roles(command)
    return response.model_dump(mode="json")


@router.post("/share", tags=["admin", "roles"])
async def grant_user_app_access(
    payload: Annotated[ShareAppPayload, Body()],
    crm_user: ResolvedCrmUserResponse = Depends(resolve_user),
    authorization_service: CrmAuthorizationServiceProtocol = Depends(get_crm_authorization_service),
) -> JsonDict:
    command = AdminCommandMapper.share_app_access_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, payload)
    )
    response = authorization_service.share_app_access(command)
    return response.model_dump(mode="json")


@router.delete("/share/{manager_id}", tags=["admin", "roles"])
async def remove_user_app_access(
    manager_id: int,
    app_scope_queries: Annotated[AppScopeQueryPayload, Query()],
    crm_user: ResolvedCrmUserResponse = Depends(resolve_user),
    authorization_service: CrmAuthorizationServiceProtocol = Depends(get_crm_authorization_service),
) -> JsonDict:
    command = AdminCommandMapper.delete_app_access_from_transport(
        GeneralMapper.transport_to_command_payload(
            crm_user,
            app_scope_queries,
            manager_id=manager_id,
        )
    )
    response = authorization_service.delete_app_access(command)
    return response.model_dump(mode="json")


@router.get("/share/", tags=["admin", "roles"])
async def list_users_with_app_access(
    app_scope_queries: Annotated[AppScopeQueryPayload, Query()],
    pagination_queries: Annotated[PaginationQueryPayload, Query()],
    crm_user: ResolvedCrmUserResponse = Depends(resolve_user),
    authorization_service: CrmAuthorizationServiceProtocol = Depends(get_crm_authorization_service),
) -> JsonDict:
    command = AdminCommandMapper.list_users_with_access_from_transport(
        GeneralMapper.transport_to_command_payload(
            crm_user,
            app_scope_queries,
            pagination_queries,
        )
    )
    response = authorization_service.list_users_with_access(command)
    return response.model_dump(mode="json")
