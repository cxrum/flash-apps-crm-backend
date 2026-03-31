from typing import Annotated, Any

from fastapi import APIRouter, Body, Depends, Query, status

from app.core.utils.general_mapper import GeneralMapper
from app.api.v1.crm.payloads import (
    AppScopeQueryPayload,
    CreateSecretTemplatePayload,
    UpdateAppSecretPayload,
    UpdateSecretTemplatePayload,
)
from app.api.v1.stubs import build_stub_response
from app.api.v1.transport import PaginationQueryPayload
from app.application.admin.secrets.mappers import SecretsResponseMapper as AdminCommandMapper
from app.application.crm_authentication.entities import ResolvedCrmUser
from app.di.dependencies import resolve_user

router = APIRouter()


@router.get("/template", tags=["admin", "secrets"])
async def list_secret_templates(
    app_scope_queries: Annotated[AppScopeQueryPayload, Query()],
    pagination_queries: Annotated[PaginationQueryPayload, Query()],
    crm_user: ResolvedCrmUser = Depends(resolve_user),
) -> dict[str, Any]:
    command = AdminCommandMapper.list_secret_templates_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, app_scope_queries, pagination_queries)
    )
    return build_stub_response(command)


@router.get("/template/{template_id}", tags=["admin", "secrets"])
async def get_secret_template(
    template_id: int,
    app_scope_queries: Annotated[AppScopeQueryPayload, Query()],
    crm_user: ResolvedCrmUser = Depends(resolve_user),
) -> dict[str, Any]:
    command = AdminCommandMapper.get_secret_template_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, app_scope_queries, template_id=template_id)
    )
    return build_stub_response(command)


@router.post("/template", status_code=status.HTTP_201_CREATED, tags=["admin", "secrets"])
async def create_secret_template(
    payload: Annotated[CreateSecretTemplatePayload, Body()],
    crm_user: ResolvedCrmUser = Depends(resolve_user),
) -> dict[str, Any]:
    command = AdminCommandMapper.create_secret_template_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, payload)
    )
    return build_stub_response(command)


@router.patch("/template/{template_id}", tags=["admin", "secrets"])
async def update_secret_template(
    template_id: int,
    app_scope_queries: Annotated[AppScopeQueryPayload, Query()],
    payload: Annotated[UpdateSecretTemplatePayload, Body()],
    crm_user: ResolvedCrmUser = Depends(resolve_user),
) -> dict[str, Any]:
    command = AdminCommandMapper.update_secret_template_from_transport(
        GeneralMapper.transport_to_command_payload(
            crm_user,
            app_scope_queries,
            payload,
            template_id=template_id,
        )
    )
    return build_stub_response(command)


@router.delete("/template/{template_id}", tags=["admin", "secrets"])
async def delete_secret_template(
    template_id: int,
    app_scope_queries: Annotated[AppScopeQueryPayload, Query()],
    crm_user: ResolvedCrmUser = Depends(resolve_user),
) -> dict[str, Any]:
    command = AdminCommandMapper.delete_secret_template_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, app_scope_queries, template_id=template_id)
    )
    return build_stub_response(command)


@router.get("/", tags=["admin", "secrets"])
async def list_app_secrets(
    app_scope_queries: Annotated[AppScopeQueryPayload, Query()],
    pagination_queries: Annotated[PaginationQueryPayload, Query()],
    crm_user: ResolvedCrmUser = Depends(resolve_user),
) -> dict[str, Any]:
    command = AdminCommandMapper.list_app_secrets_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, app_scope_queries, pagination_queries)
    )
    return build_stub_response(command)


@router.get("/{secret_id}", tags=["admin", "secrets"])
async def get_app_secret(
    secret_id: int,
    app_scope_queries: Annotated[AppScopeQueryPayload, Query()],
    crm_user: ResolvedCrmUser = Depends(resolve_user),
) -> dict[str, Any]:
    command = AdminCommandMapper.get_app_secret_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, app_scope_queries, app_secret_id=secret_id)
    )
    return build_stub_response(command)


@router.patch("/{secret_id}", tags=["admin", "secrets"])
async def update_app_secret(
    secret_id: int,
    app_scope_queries: Annotated[AppScopeQueryPayload, Query()],
    payload: Annotated[UpdateAppSecretPayload, Body()],
    crm_user: ResolvedCrmUser = Depends(resolve_user),
) -> dict[str, Any]:
    command = AdminCommandMapper.update_app_secret_from_transport(
        GeneralMapper.transport_to_command_payload(
            crm_user,
            app_scope_queries,
            payload,
            secret_id=secret_id,
        )
    )
    return build_stub_response(command)


@router.delete("/{secret_id}", tags=["admin", "secrets"])
async def delete_app_secret(
    secret_id: int,
    app_scope_queries: Annotated[AppScopeQueryPayload, Query()],
    crm_user: ResolvedCrmUser = Depends(resolve_user),
) -> dict[str, Any]:
    command = AdminCommandMapper.delete_app_secret_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, app_scope_queries, secret_id=secret_id)
    )
    return build_stub_response(command)
