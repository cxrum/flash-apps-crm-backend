from typing import Annotated, Any

from fastapi import APIRouter, Body, Depends, Query, status

from app.modules.crm.api.v1.crm.payloads import (
    AppFilterQueryPayload,
    CreatePushCampaignPayload,
    SdkPushRegisterPayload,
    UpdatePushCampaignPayload,
)
from app.modules.crm.api.v1.stubs import build_stub_response
from app.modules.crm.api.v1.transport import PaginationQueryPayload
from app.modules.crm.application.admin.push.mappers import PushResponseMapper as AdminCommandMapper
from app.modules.crm.application.admin.push.protocol import PushServiceProtocol
from app.modules.crm.application.base import JsonDict
from app.modules.crm.application.crm_authentication.responses import ResolvedCrmUserResponse
from app.modules.crm.core.utils.general_mapper import GeneralMapper
from app.modules.crm.di.dependencies import resolve_user
from app.modules.crm.di.services import get_push_service

router = APIRouter()


@router.get("/", tags=["admin", "push"])
async def list_push_campaigns(
    app_filter_queries: Annotated[AppFilterQueryPayload, Query()],
    pagination_queries: Annotated[PaginationQueryPayload, Query()],
    crm_user: ResolvedCrmUserResponse = Depends(resolve_user),
    push_service: PushServiceProtocol = Depends(get_push_service),
) -> JsonDict:
    command = AdminCommandMapper.list_push_campaigns_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, app_filter_queries, pagination_queries)
    )

    response = push_service.list(command)

    return response.model_dump(mode="json")


@router.get("/{push_id}", tags=["admin", "push"])
async def get_push_campaign(
    push_id: int,
    app_filter_queries: Annotated[AppFilterQueryPayload, Query()],
    crm_user: ResolvedCrmUserResponse = Depends(resolve_user),
    push_service: PushServiceProtocol = Depends(get_push_service),
) -> JsonDict:
    command = AdminCommandMapper.get_push_campaign_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, app_filter_queries, push_id=push_id)
    )
    response = push_service.get(command)

    return response.model_dump(mode="json")


@router.post("/", status_code=status.HTTP_201_CREATED, tags=["admin", "push"])
async def create_push_campaign(
    payload: Annotated[CreatePushCampaignPayload, Body()],
    crm_user: ResolvedCrmUserResponse = Depends(resolve_user),
    push_service: PushServiceProtocol = Depends(get_push_service),
) -> JsonDict:
    command = AdminCommandMapper.create_push_campaign_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, payload)
    )
    response = push_service.create(command)

    return response.model_dump(mode="json")


@router.patch("/{push_id}", tags=["admin", "push"])
async def update_push_campaign(
    push_id: int,
    app_filter_queries: Annotated[AppFilterQueryPayload, Query()],
    payload: Annotated[UpdatePushCampaignPayload, Body()],
    crm_user: ResolvedCrmUserResponse = Depends(resolve_user),
    push_service: PushServiceProtocol = Depends(get_push_service),
) -> JsonDict:
    command = AdminCommandMapper.update_push_campaign_from_transport(
        GeneralMapper.transport_to_command_payload(
            crm_user,
            app_filter_queries,
            payload,
            push_id=push_id,
        )
    )
    response = push_service.update(command)

    return response.model_dump(mode="json")


@router.delete("/{push_id}", tags=["admin", "push"])
async def delete_push_campaign(
    push_id: int,
    app_filter_queries: Annotated[AppFilterQueryPayload, Query()],
    crm_user: ResolvedCrmUserResponse = Depends(resolve_user),
    push_service: PushServiceProtocol = Depends(get_push_service),
) -> JsonDict:
    command = AdminCommandMapper.delete_push_campaign_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, app_filter_queries, push_id=push_id)
    )
    response = push_service.delete(command)

    return response.model_dump(mode="json")


@router.post("/{push_id}/start", tags=["admin", "push"])
async def start_push_campaign(
    push_id: int,
    app_filter_queries: Annotated[AppFilterQueryPayload, Query()],
    crm_user: ResolvedCrmUserResponse = Depends(resolve_user),
    push_service: PushServiceProtocol = Depends(get_push_service),
) -> JsonDict:
    command = AdminCommandMapper.start_push_campaign_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, app_filter_queries, push_id=push_id)
    )
    return build_stub_response(command)  # type: ignore


@router.post("/register", status_code=status.HTTP_202_ACCEPTED, tags=["sdk"])
async def register_push_token(
    payload: SdkPushRegisterPayload, push_service: PushServiceProtocol = Depends(get_push_service)
) -> JsonDict:
    command = AdminCommandMapper.push_register_from_transport(GeneralMapper.to_dict(payload))

    response = push_service.register_device(command)

    return response.model_dump(mode="json")
