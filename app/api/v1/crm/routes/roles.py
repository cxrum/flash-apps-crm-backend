from typing import Annotated, Any

from fastapi import APIRouter, Body, Depends, Query

from app.core.utils.general_mapper import GeneralMapper
from app.api.v1.crm.payloads import AppFilterQueryPayload, RolesQueryPayload, ShareAppPayload
from app.api.v1.stubs import build_stub_response
from app.api.v1.transport import PaginationQueryPayload
from app.application.admin.crm_authorization.mappers import AuthenticationResponseMapper as AdminCommandMapper
from app.application.crm_authentication.entities import ResolvedCrmUser
from app.di.dependencies import resolve_user

router = APIRouter()


@router.get("/", tags=["admin", "roles"])
async def list_roles(
    pagination_queries: Annotated[PaginationQueryPayload, Query()],
    role_queries: Annotated[RolesQueryPayload, Query()],
    crm_user: ResolvedCrmUser = Depends(resolve_user),
) -> str:
    command = AdminCommandMapper.list_roles_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, role_queries, pagination_queries)
    )
    return build_stub_response(command)


@router.post("/share", tags=["admin", "roles"])
async def grant_user_app_access(
    payload: Annotated[ShareAppPayload, Body()],
    crm_user: ResolvedCrmUser = Depends(resolve_user),
) -> str:
    command = AdminCommandMapper.share_app_access_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, payload)
    )
    return build_stub_response(command)


@router.delete("/share/{manager_id}", tags=["admin", "roles"])
async def remove_user_app_access(
    manager_id: int,
    app_filter_queries: Annotated[AppFilterQueryPayload, Query()],
    crm_user: ResolvedCrmUser = Depends(resolve_user),
) -> str:
    command = AdminCommandMapper.delete_app_access_from_transport(
        GeneralMapper.transport_to_command_payload(
            crm_user,
            app_filter_queries,
            manager_id=manager_id,
        )
    )
    return build_stub_response(command)


@router.get("/share/{role_code}", tags=["admin", "roles"])
async def list_users_with_app_access(
    role_code: str,
    app_filter_queries: Annotated[AppFilterQueryPayload, Query()],
    pagination_queries: Annotated[PaginationQueryPayload, Query()],
    crm_user: ResolvedCrmUser = Depends(resolve_user),
) -> str:
    command = AdminCommandMapper.list_users_with_access_from_transport(
        GeneralMapper.transport_to_command_payload(
            crm_user,
            app_filter_queries,
            pagination_queries,
            role_code=role_code,
        )
    )
    return build_stub_response(command)
