from typing import Annotated

from fastapi import APIRouter, Body, Depends, Query, status

from app.modules.crm.api.v1.crm.payloads import (
    AppScopeQueryPayload,
    CreateConversionDefinitionPayload,
    UpdateConversionDefinitionPayload,
)
from app.modules.crm.api.v1.transport import PaginationQueryPayload
from app.modules.crm.application.admin.definitions.mappers import DefinitionsCommandsMapper
from app.modules.crm.application.admin.definitions.protocol import DefinitionsServiceProtocol
from app.modules.crm.application.base import JsonDict
from app.modules.crm.application.crm_authentication.responses import ResolvedCrmUserResponse
from app.modules.crm.core.utils.general_mapper import GeneralMapper
from app.modules.crm.di.dependencies import resolve_user
from app.modules.crm.di.services import get_admin_definitions_service

router = APIRouter()


@router.get("/", tags=["admin", "conversion"])
async def list_conversions(
    app_scope_queries: Annotated[AppScopeQueryPayload, Query()],
    pagination_queries: Annotated[PaginationQueryPayload, Query()],
    crm_user: ResolvedCrmUserResponse = Depends(resolve_user),
    definition_service: DefinitionsServiceProtocol = Depends(get_admin_definitions_service),
) -> JsonDict:
    command = DefinitionsCommandsMapper.list_conversions_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, app_scope_queries, pagination_queries)
    )

    response = definition_service.list_conversions(command)
    return response.model_dump(mode="json")


@router.get("/{conversion_definition_id}", tags=["admin", "conversion"])
async def get_conversion(
    conversion_definition_id: int,
    app_scope_queries: Annotated[AppScopeQueryPayload, Query()],
    crm_user: ResolvedCrmUserResponse = Depends(resolve_user),
    definition_service: DefinitionsServiceProtocol = Depends(get_admin_definitions_service),
) -> JsonDict:
    command = DefinitionsCommandsMapper.get_conversion_from_transport(
        GeneralMapper.transport_to_command_payload(
            crm_user,
            app_scope_queries,
            conversion_definition_id=conversion_definition_id,
        )
    )
    response = definition_service.get_conversion_definition(command)
    return response.model_dump(mode="json")


@router.post("/", status_code=status.HTTP_201_CREATED, tags=["admin", "conversion"])
async def create_conversion(
    payload: Annotated[CreateConversionDefinitionPayload, Body()],
    crm_user: ResolvedCrmUserResponse = Depends(resolve_user),
    definition_service: DefinitionsServiceProtocol = Depends(get_admin_definitions_service),
) -> JsonDict:
    command = DefinitionsCommandsMapper.create_conversion_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, payload)
    )
    response = definition_service.create_conversion_definition(command)
    return response.model_dump(mode="json")


@router.delete("/{conversion_definition_id}", tags=["admin", "conversion"])
async def delete_conversion(
    conversion_definition_id: int,
    app_scope_queries: Annotated[AppScopeQueryPayload, Query()],
    crm_user: ResolvedCrmUserResponse = Depends(resolve_user),
    definition_service: DefinitionsServiceProtocol = Depends(get_admin_definitions_service),
) -> JsonDict:
    command = DefinitionsCommandsMapper.delete_conversion_from_transport(
        GeneralMapper.transport_to_command_payload(
            crm_user,
            app_scope_queries,
            conversion_definition_id=conversion_definition_id,
        )
    )
    response = definition_service.delete_conversion_definition(command)
    return response.model_dump(mode="json")


@router.patch("/{conversion_definition_id}", tags=["admin", "metrics"])
async def update_conversion(
    conversion_definition_id: int,
    app_scope_queries: Annotated[AppScopeQueryPayload, Query()],
    payload: Annotated[UpdateConversionDefinitionPayload, Body()],
    crm_user: ResolvedCrmUserResponse = Depends(resolve_user),
    definition_service: DefinitionsServiceProtocol = Depends(get_admin_definitions_service),
) -> JsonDict:
    command = DefinitionsCommandsMapper.update_conversion_from_transport(
        GeneralMapper.transport_to_command_payload(
            crm_user,
            app_scope_queries,
            payload,
            conversion_definition_id=conversion_definition_id,
        )
    )
    response = definition_service.update_conversion_definition(command)
    return response.model_dump(mode="json")
