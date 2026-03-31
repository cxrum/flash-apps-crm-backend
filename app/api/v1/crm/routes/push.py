from typing import Annotated, Any

from fastapi import APIRouter, Body, Depends, Query, status

from app.core.utils.general_mapper import GeneralMapper
from app.api.v1.crm.payloads import (
    AppFilterQueryPayload,
    CreatePushCampaignPayload,
    UpdatePushCampaignPayload,
)
from app.api.v1.stubs import build_stub_response
from app.api.v1.transport import PaginationQueryPayload
from app.application.admin.push.mappers import PushResponseMapper as AdminCommandMapper
from app.application.crm_authentication.entities import ResolvedCrmUser
from app.di.dependencies import resolve_user

router = APIRouter()


@router.get("/", tags=["admin", "push"])
async def list_push_campaigns(
    app_filter_queries: Annotated[AppFilterQueryPayload, Query()],
    pagination_queries: Annotated[PaginationQueryPayload, Query()],
    crm_user: ResolvedCrmUser = Depends(resolve_user),
) -> dict[str, Any]:
    command = AdminCommandMapper.list_push_campaigns_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, app_filter_queries, pagination_queries)
    )
    return build_stub_response(command)


@router.get("/{push_id}", tags=["admin", "push"])
async def get_push_campaign(
    push_id: int,
    app_filter_queries: Annotated[AppFilterQueryPayload, Query()],
    crm_user: ResolvedCrmUser = Depends(resolve_user),
) -> dict[str, Any]:
    command = AdminCommandMapper.get_push_campaign_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, app_filter_queries, push_id=push_id)
    )
    return build_stub_response(command)


@router.post("/", status_code=status.HTTP_201_CREATED, tags=["admin", "push"])
async def create_push_campaign(
    payload: Annotated[CreatePushCampaignPayload, Body()],
    crm_user: ResolvedCrmUser = Depends(resolve_user),
) -> dict[str, Any]:
    command = AdminCommandMapper.create_push_campaign_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, payload)
    )
    return build_stub_response(command)


@router.patch("/{push_id}", tags=["admin", "push"])
async def update_push_campaign(
    push_id: int,
    app_filter_queries: Annotated[AppFilterQueryPayload, Query()],
    payload: Annotated[UpdatePushCampaignPayload, Body()],
    crm_user: ResolvedCrmUser = Depends(resolve_user),
) -> dict[str, Any]:
    command = AdminCommandMapper.update_push_campaign_from_transport(
        GeneralMapper.transport_to_command_payload(
            crm_user,
            app_filter_queries,
            payload,
            push_id=push_id,
        )
    )
    return build_stub_response(command)


@router.delete("/{push_id}", tags=["admin", "push"])
async def delete_push_campaign(
    push_id: int,
    app_filter_queries: Annotated[AppFilterQueryPayload, Query()],
    crm_user: ResolvedCrmUser = Depends(resolve_user),
) -> dict[str, Any]:
    command = AdminCommandMapper.delete_push_campaign_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, app_filter_queries, push_id=push_id)
    )
    return build_stub_response(command)


@router.post("/{push_id}/start", tags=["admin", "push"])
async def start_push_campaign(
    push_id: int,
    app_filter_queries: Annotated[AppFilterQueryPayload, Query()],
    crm_user: ResolvedCrmUser = Depends(resolve_user),
) -> dict[str, Any]:
    command = AdminCommandMapper.start_push_campaign_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, app_filter_queries, push_id=push_id)
    )
    return build_stub_response(command)
