from typing import Annotated, Any

from fastapi import APIRouter, Body, Depends, Query, status

from app.api.v1.crm.payloads import (
    AppScopeQueryPayload,
    CreateMetricDefinitionPayload,
    UpdateMetricDefinitionPayload,
)
from app.api.v1.stubs import build_stub_response
from app.api.v1.transport import PaginationQueryPayload
from app.application.admin.definitions.mappers import DefinitionsCommandsMapper
from app.application.crm_authentication.entities import ResolvedCrmUser
from app.core.utils.general_mapper import GeneralMapper
from app.di.dependencies import resolve_user

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, tags=["admin", "metrics"])
async def create_metric(
    payload: Annotated[CreateMetricDefinitionPayload, Body()],
    crm_user: ResolvedCrmUser = Depends(resolve_user),
) -> dict[str, Any]:
    command = DefinitionsCommandsMapper.create_metric_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, payload)
    )
    return build_stub_response(command)


@router.get("/", tags=["admin", "metrics"])
async def list_metrics(
    app_scope_queries: Annotated[AppScopeQueryPayload, Query()],
    pagination_queries: Annotated[PaginationQueryPayload, Query()],
    crm_user: ResolvedCrmUser = Depends(resolve_user),
) -> dict[str, Any]:
    command = DefinitionsCommandsMapper.list_metrics_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, app_scope_queries, pagination_queries)
    )
    return build_stub_response(command)


@router.get("/{metric_definition_id}", tags=["admin", "metrics"])
async def get_metric(
    metric_definition_id: int,
    app_scope_queries: Annotated[AppScopeQueryPayload, Query()],
    crm_user: ResolvedCrmUser = Depends(resolve_user),
) -> dict[str, Any]:
    command = DefinitionsCommandsMapper.get_metric_from_transport(
        GeneralMapper.transport_to_command_payload(
            crm_user,
            app_scope_queries,
            metric_definition_id=metric_definition_id,
        )
    )
    return build_stub_response(command)


@router.patch("/{metric_definition_id}", tags=["admin", "metrics"])
async def update_metric(
    metric_definition_id: int,
    app_scope_queries: Annotated[AppScopeQueryPayload, Query()],
    payload: Annotated[UpdateMetricDefinitionPayload, Body()],
    crm_user: ResolvedCrmUser = Depends(resolve_user),
) -> dict[str, Any]:
    command = DefinitionsCommandsMapper.update_metric_from_transport(
        GeneralMapper.transport_to_command_payload(
            crm_user,
            app_scope_queries,
            payload,
            metric_definition_id=metric_definition_id,
        )
    )
    return build_stub_response(command)


@router.delete("/{metric_definition_id}", tags=["admin", "metrics"])
async def delete_metric(
    metric_definition_id: int,
    app_scope_queries: Annotated[AppScopeQueryPayload, Query()],
    crm_user: ResolvedCrmUser = Depends(resolve_user),
) -> dict[str, Any]:
    command = DefinitionsCommandsMapper.delete_metric_from_transport(
        GeneralMapper.transport_to_command_payload(
            crm_user,
            app_scope_queries,
            metric_definition_id=metric_definition_id,
        )
    )
    return build_stub_response(command)
