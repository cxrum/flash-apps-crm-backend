from typing import Annotated, Any

from fastapi import APIRouter, Body, Depends, Query, status

from app.core.utils.general_mapper import GeneralMapper
from app.api.v1.crm.payloads import (
    AppFilterQueryPayload,
    CreatePostbackRulePayload,
    UpdatePostbackRulePayload,
)
from app.api.v1.transport import PaginationQueryPayload
from app.application.admin.postback.mappers import PostbackResponseMapper as AdminCommandMapper
from app.application.admin.postback.service import PostbackService
from app.application.crm_authentication.responses import ResolvedCrmUserResponse
from app.di.dependencies import get_admin_postback_service, resolve_user

router = APIRouter()

@router.get("/", tags=["admin", "postback"])
async def list_postbacks(
    app_filter_queries: Annotated[AppFilterQueryPayload, Query()],
    pagination_queries: Annotated[PaginationQueryPayload, Query()],
    crm_user: ResolvedCrmUserResponse = Depends(resolve_user),
    postback_service: PostbackService = Depends(get_admin_postback_service),
) -> str:
    command = AdminCommandMapper.list_postbacks_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, app_filter_queries, pagination_queries)
    )
    response = postback_service.get_list_postbacks(command)
    return response.model_dump_json()


@router.get("/{postback_id}", tags=["admin", "postback"])
async def get_postback(
    postback_id: int,
    app_filter_queries: Annotated[AppFilterQueryPayload, Query()],
    crm_user: ResolvedCrmUserResponse = Depends(resolve_user),
    postback_service: PostbackService = Depends(get_admin_postback_service),
) -> str:
    command = AdminCommandMapper.get_postback_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, app_filter_queries, postback_id=postback_id)
    )
    response = postback_service.get_postback(command)
    return response.model_dump_json()


@router.patch("/{postback_id}", tags=["admin", "postback"])
async def update_postback(
    postback_id: int,
    app_filter_queries: Annotated[AppFilterQueryPayload, Query()],
    payload: Annotated[UpdatePostbackRulePayload, Body()],
    crm_user: ResolvedCrmUserResponse = Depends(resolve_user),
    postback_service: PostbackService = Depends(get_admin_postback_service),
) -> str:
    command = AdminCommandMapper.update_postback_from_transport(
        GeneralMapper.transport_to_command_payload(
            crm_user,
            app_filter_queries,
            payload,
            postback_id=postback_id,
        )
    )
    response = postback_service.update_postback(command)
    return response.model_dump_json()


@router.delete("/{postback_id}", tags=["admin", "postback"])
async def delete_postback(
    postback_id: int,
    app_filter_queries: Annotated[AppFilterQueryPayload, Query()],
    crm_user: ResolvedCrmUserResponse = Depends(resolve_user),
    postback_service: PostbackService = Depends(get_admin_postback_service),
) -> str:
    command = AdminCommandMapper.delete_postback_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, app_filter_queries, postback_id=postback_id)
    )
    response = postback_service.delete_postback(command)
    return response.model_dump_json()


@router.post("/", status_code=status.HTTP_201_CREATED, tags=["admin", "postback"])
async def create_postback(
    payload: Annotated[CreatePostbackRulePayload, Body()],
    crm_user: ResolvedCrmUserResponse = Depends(resolve_user),
    postback_service: PostbackService = Depends(get_admin_postback_service),
) -> str:
    command = AdminCommandMapper.create_postback_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, payload)
    )
    response = postback_service.create_postback(command)
    return response.model_dump_json()
