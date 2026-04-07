from typing import Annotated, Any

from fastapi import APIRouter, Body, Depends, Query, status

from app.api.v1.crm.payloads import (
    AppScopeQueryPayload,
    CreateMetricDefinitionPayload,
    UpdateMetricDefinitionPayload,
)
from app.api.v1.transport import PaginationQueryPayload
from app.application.admin.definitions.mappers import DefinitionsCommandsMapper
from app.application.admin.definitions.service import DefinitionsService
from app.application.crm_authentication.responses import ResolvedCrmUserResponse
from app.core.utils.general_mapper import GeneralMapper
from app.di.dependencies import resolve_user
from app.di.services import get_admin_definitions_service

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, tags=["admin", "metrics"])
async def create_metric(
    payload: Annotated[CreateMetricDefinitionPayload, Body()],
    crm_user: ResolvedCrmUserResponse = Depends(resolve_user),
    definition_service: DefinitionsService = Depends(get_admin_definitions_service),
) -> str:
    command = DefinitionsCommandsMapper.create_metric_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, payload)
    )
    response = definition_service.create_metric_definition(command)
    return response.model_dump_json()


@router.get("/", tags=["admin", "metrics"])
async def list_metrics(
    app_scope_queries: Annotated[AppScopeQueryPayload, Query()],
    pagination_queries: Annotated[PaginationQueryPayload, Query()],
    crm_user: ResolvedCrmUserResponse = Depends(resolve_user),
    definition_service: DefinitionsService = Depends(get_admin_definitions_service),
) -> str:
    command = DefinitionsCommandsMapper.list_metrics_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, app_scope_queries, pagination_queries)
    )
    response = definition_service.list_metrics(command)
    return response.model_dump_json()


@router.get("/{metric_definition_id}", tags=["admin", "metrics"])
async def get_metric(
    metric_definition_id: int,
    app_scope_queries: Annotated[AppScopeQueryPayload, Query()],
    crm_user: ResolvedCrmUserResponse = Depends(resolve_user),
    definition_service: DefinitionsService = Depends(get_admin_definitions_service),
) -> str:
    command = DefinitionsCommandsMapper.get_metric_from_transport(
        GeneralMapper.transport_to_command_payload(
            crm_user,
            app_scope_queries,
            metric_definition_id=metric_definition_id,
        )
    )
    response = definition_service.get_metric_definition(command)
    return response.model_dump_json()


@router.patch("/{metric_definition_id}", tags=["admin", "metrics"])
async def update_metric(
    metric_definition_id: int,
    app_scope_queries: Annotated[AppScopeQueryPayload, Query()],
    payload: Annotated[UpdateMetricDefinitionPayload, Body()],
    crm_user: ResolvedCrmUserResponse = Depends(resolve_user),
    definition_service: DefinitionsService = Depends(get_admin_definitions_service),
) -> str:
    command = DefinitionsCommandsMapper.update_metric_from_transport(
        GeneralMapper.transport_to_command_payload(
            crm_user,
            app_scope_queries,
            payload,
            metric_definition_id=metric_definition_id,
        )
    )
    response = definition_service.update_metric_definition(command)
    return response.model_dump_json()


@router.delete("/{metric_definition_id}", tags=["admin", "metrics"])
async def delete_metric(
    metric_definition_id: int,
    app_scope_queries: Annotated[AppScopeQueryPayload, Query()],
    crm_user: ResolvedCrmUserResponse = Depends(resolve_user),
    definition_service: DefinitionsService = Depends(get_admin_definitions_service),
) -> str:
    command = DefinitionsCommandsMapper.delete_metric_from_transport(
        GeneralMapper.transport_to_command_payload(
            crm_user,
            app_scope_queries,
            metric_definition_id=metric_definition_id,
        )
    )
    response = definition_service.delete_metric_definition(command)
    return response.model_dump_json()
