from typing import Annotated, Any

from fastapi import APIRouter, Body, Depends, Query, status

from app.api.v1.crm.payloads import (
    AppScopeQueryPayload,
    CreateParamDefinitionPayload,
    UpdateParamDefinitionPayload,
)
from app.api.v1.stubs import build_stub_response
from app.api.v1.transport import PaginationQueryPayload
from app.application.admin.definitions.mappers import DefinitionsCommandsMapper
from app.application.crm_authentication.entities import ResolvedCrmUser
from app.core.utils.general_mapper import GeneralMapper
from app.di.dependencies import resolve_user

router = APIRouter()


@router.get("/", tags=["admin", "params"])
async def list_params(
    app_scope_queries: Annotated[AppScopeQueryPayload, Query()],
    pagination_queries: Annotated[PaginationQueryPayload, Query()],
    crm_user: ResolvedCrmUser = Depends(resolve_user),
) -> dict[str, Any]:
    command = DefinitionsCommandsMapper.list_params_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, app_scope_queries, pagination_queries)
    )
    return build_stub_response(command)


@router.get("/{param_definition_id}", tags=["admin", "params"])
async def get_param(
    param_definition_id: int,
    app_scope_queries: Annotated[AppScopeQueryPayload, Query()],
    crm_user: ResolvedCrmUser = Depends(resolve_user),
) -> dict[str, Any]:
    command = DefinitionsCommandsMapper.get_param_from_transport(
        GeneralMapper.transport_to_command_payload(
            crm_user,
            app_scope_queries,
            param_definition_id=param_definition_id,
        )
    )
    return build_stub_response(command)


@router.patch("/{param_definition_id}", tags=["admin", "params"])
async def update_param(
    param_definition_id: int,
    app_scope_queries: Annotated[AppScopeQueryPayload, Query()],
    payload: Annotated[UpdateParamDefinitionPayload, Body()],
    crm_user: ResolvedCrmUser = Depends(resolve_user),
) -> dict[str, Any]:
    command = DefinitionsCommandsMapper.update_param_from_transport(
        GeneralMapper.transport_to_command_payload(
            crm_user,
            app_scope_queries,
            payload,
            param_definition_id=param_definition_id,
        )
    )
    return build_stub_response(command)


@router.post("/", status_code=status.HTTP_201_CREATED, tags=["admin", "params"])
async def create_param(
    payload: Annotated[CreateParamDefinitionPayload, Body()],
    crm_user: ResolvedCrmUser = Depends(resolve_user),
) -> dict[str, Any]:
    command = DefinitionsCommandsMapper.create_param_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, payload)
    )
    return build_stub_response(command)


@router.delete("/{param_definition_id}", tags=["admin", "params"])
async def delete_param(
    param_definition_id: int,
    app_scope_queries: Annotated[AppScopeQueryPayload, Query()],
    crm_user: ResolvedCrmUser = Depends(resolve_user),
) -> dict[str, Any]:
    command = DefinitionsCommandsMapper.delete_param_from_transport(
        GeneralMapper.transport_to_command_payload(
            crm_user,
            app_scope_queries,
            param_definition_id=param_definition_id,
        )
    )
    return build_stub_response(command)
