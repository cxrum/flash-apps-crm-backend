from typing import Annotated, Any

from fastapi import APIRouter, Body, Depends, Query, status

from app.core.utils.general_mapper import GeneralMapper as GeneralMapper
from app.api.v1.crm.payloads import (
    AppFilterQueryPayload,
    CreatePostbackRulePayload,
    UpdatePostbackRulePayload,
)
from app.api.v1.stubs import build_stub_response
from app.api.v1.transport import PaginationQueryPayload
from app.application.admin.postback.mappers import PostbackResponseMapper as AdminCommandMapper
from app.application.crm_authentication.entities import ResolvedCrmUser
from app.di.dependencies import resolve_user

router = APIRouter()

@router.get("/", tags=["admin", "postback"])
async def list_postbacks(
    app_filter_queries: Annotated[AppFilterQueryPayload, Query()],
    pagination_queries: Annotated[PaginationQueryPayload, Query()],
    crm_user: ResolvedCrmUser = Depends(resolve_user),
) -> dict[str, Any]:
    command = AdminCommandMapper.list_postbacks_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, app_filter_queries, pagination_queries)
    )
    return build_stub_response(command)


@router.get("/{postback_id}", tags=["admin", "postback"])
async def get_postback(
    postback_id: int,
    app_filter_queries: Annotated[AppFilterQueryPayload, Query()],
    crm_user: ResolvedCrmUser = Depends(resolve_user),
) -> dict[str, Any]:
    command = AdminCommandMapper.get_postback_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, app_filter_queries, postback_id=postback_id)
    )
    return build_stub_response(command)


@router.patch("/{postback_id}", tags=["admin", "postback"])
async def update_postback(
    postback_id: int,
    app_filter_queries: Annotated[AppFilterQueryPayload, Query()],
    payload: Annotated[UpdatePostbackRulePayload, Body()],
    crm_user: ResolvedCrmUser = Depends(resolve_user),
) -> dict[str, Any]:
    command = AdminCommandMapper.update_postback_from_transport(
        GeneralMapper.transport_to_command_payload(
            crm_user,
            app_filter_queries,
            payload,
            postback_id=postback_id,
        )
    )
    return build_stub_response(command)


@router.delete("/{postback_id}", tags=["admin", "postback"])
async def delete_postback(
    postback_id: int,
    app_filter_queries: Annotated[AppFilterQueryPayload, Query()],
    crm_user: ResolvedCrmUser = Depends(resolve_user),
) -> dict[str, Any]:
    command = AdminCommandMapper.delete_postback_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, app_filter_queries, postback_id=postback_id)
    )
    return build_stub_response(command)


@router.post("/", status_code=status.HTTP_201_CREATED, tags=["admin", "postback"])
async def create_postback(
    payload: Annotated[CreatePostbackRulePayload, Body()],
    crm_user: ResolvedCrmUser = Depends(resolve_user),
) -> dict[str, Any]:
    command = AdminCommandMapper.create_postback_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, payload)
    )
    return build_stub_response(command)
