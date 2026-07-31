from typing import Annotated, Any

from fastapi import APIRouter, Body, Depends, Query, status

from app.core.utils.general_mapper import GeneralMapper
from app.modules.crm.api.v1.crm.payloads import (
    AppScopeQueryPayload,
    CreateParamDefinitionPayload,
    UpdateParamDefinitionPayload,
)
from app.modules.crm.api.v1.transport import PaginationQueryPayload
from app.modules.crm.application.admin.definitions.mappers import DefinitionsCommandsMapper
from app.modules.crm.application.admin.definitions.protocol import DefinitionsServiceProtocol
from app.modules.crm.application.base import JsonDict
from app.modules.crm.application.crm_authentication.responses import ResolvedCrmUserResponse
from app.modules.crm.di.dependencies import resolve_user
from app.modules.crm.di.services import get_admin_definitions_service

router = APIRouter()


@router.get("/", tags=["admin", "params"])
async def list_params(
    app_scope_queries: Annotated[AppScopeQueryPayload, Query()],
    pagination_queries: Annotated[PaginationQueryPayload, Query()],
    crm_user: Annotated[ResolvedCrmUserResponse, Depends(resolve_user)],
    definition_service: Annotated[DefinitionsServiceProtocol, Depends(get_admin_definitions_service)],
) -> JsonDict:
    command = DefinitionsCommandsMapper.list_params_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, app_scope_queries, pagination_queries)
    )
    response = definition_service.list_params(command)
    return response.model_dump(mode="json")


@router.get("/{param_definition_id}", tags=["admin", "params"])
async def get_param(
    param_definition_id: int,
    app_scope_queries: Annotated[AppScopeQueryPayload, Query()],
    crm_user: Annotated[ResolvedCrmUserResponse, Depends(resolve_user)],
    definition_service: Annotated[DefinitionsServiceProtocol, Depends(get_admin_definitions_service)],
) -> JsonDict:
    command = DefinitionsCommandsMapper.get_param_from_transport(
        GeneralMapper.transport_to_command_payload(
            crm_user,
            app_scope_queries,
            param_definition_id=param_definition_id,
        )
    )
    response = definition_service.get_param_definition(command)
    return response.model_dump(mode="json")


@router.patch("/{param_definition_id}", tags=["admin", "params"])
async def update_param(
    param_definition_id: int,
    app_scope_queries: Annotated[AppScopeQueryPayload, Query()],
    payload: Annotated[UpdateParamDefinitionPayload, Body()],
    crm_user: Annotated[ResolvedCrmUserResponse, Depends(resolve_user)],
    definition_service: Annotated[DefinitionsServiceProtocol, Depends(get_admin_definitions_service)],
) -> JsonDict:
    command = DefinitionsCommandsMapper.update_param_from_transport(
        GeneralMapper.transport_to_command_payload(
            crm_user,
            app_scope_queries,
            payload,
            param_definition_id=param_definition_id,
        )
    )
    response = definition_service.update_param_definition(command)
    return response.model_dump(mode="json")


@router.post("/", status_code=status.HTTP_201_CREATED, tags=["admin", "params"])
async def create_param(
    payload: Annotated[CreateParamDefinitionPayload, Body()],
    crm_user: Annotated[ResolvedCrmUserResponse, Depends(resolve_user)],
    definition_service: Annotated[DefinitionsServiceProtocol, Depends(get_admin_definitions_service)],
) -> JsonDict:
    command = DefinitionsCommandsMapper.create_param_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, payload)
    )
    response = definition_service.create_param_definition(command)
    return response.model_dump()


@router.delete("/{param_definition_id}", tags=["admin", "params"])
async def delete_param(
    param_definition_id: int,
    app_scope_queries: Annotated[AppScopeQueryPayload, Query()],
    crm_user: Annotated[ResolvedCrmUserResponse, Depends(resolve_user)],
    definition_service: Annotated[DefinitionsServiceProtocol, Depends(get_admin_definitions_service)],
) -> JsonDict:
    command = DefinitionsCommandsMapper.delete_param_from_transport(
        GeneralMapper.transport_to_command_payload(
            crm_user,
            app_scope_queries,
            param_definition_id=param_definition_id,
        )
    )
    response = definition_service.delete_param_definition(command)
    return response.model_dump()
