from dataclasses import asdict
from typing import Annotated, Any

from fastapi import APIRouter, Body, Depends, Query, status

from app.api.v1.crm.payloads import (
    CreateAppPayload,
    CreateAppPlatformPayload,
    DeleteAppPayload,
    UpdateAppPayload,
    UpdateAppPlatformPayload,
)
from app.api.v1.stubs import build_stub_response
from app.api.v1.transport import PaginationQueryPayload
from app.application.crm_authentication.entities import ResolvedCrmUser
from app.application.sdk.apps.mappers import SdkAppCommandsMapper
from app.application.sdk.apps.service import AppService
from app.core.utils.general_mapper import GeneralMapper
from app.di.dependencies import get_sdk_app_service, resolve_user

router = APIRouter()


@router.get("/{app_id}", tags=["admin", "app"])
async def get_app(
    app_id: int,
    crm_user: ResolvedCrmUser = Depends(resolve_user),
    
    app_service: AppService = Depends(get_sdk_app_service)
) -> dict[str, Any]:
    command = SdkAppCommandsMapper.get_app_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, app_id=app_id)
    )
    
    response = app_service.get_app(command)

    return asdict(response) 


@router.get("/", tags=["admin", "app"])
async def list_apps(
    pagination_queries: Annotated[PaginationQueryPayload, Query()],
    crm_user: ResolvedCrmUser = Depends(resolve_user),
    
    app_service: AppService = Depends(get_sdk_app_service)
) -> dict[str, Any]:
    command = SdkAppCommandsMapper.list_apps_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, pagination_queries)
    )
    
    response = app_service.get_apps(command)

    return asdict(response) 

@router.post("/", status_code=status.HTTP_201_CREATED, tags=["admin", "app"])
async def create_app(
    payload: Annotated[CreateAppPayload, Body()],
    crm_user: ResolvedCrmUser = Depends(resolve_user),
    
    app_service: AppService = Depends(get_sdk_app_service)
) -> dict[str, Any]:
    command = SdkAppCommandsMapper.create_app_from_transport(GeneralMapper.transport_to_command_payload(crm_user, payload))
    
    response = app_service.create_app(command)

    return asdict(response) 


@router.patch("/", status_code=status.HTTP_201_CREATED, tags=["admin", "app"])
async def update_app(
    payload: Annotated[UpdateAppPayload, Body()],
    crm_user: ResolvedCrmUser = Depends(resolve_user),
) -> dict[str, Any]:
    command = SdkAppCommandsMapper.update_app_from_transport(GeneralMapper.transport_to_command_payload(crm_user, payload))
    return build_stub_response(command)


@router.delete("/", status_code=status.HTTP_201_CREATED, tags=["admin", "app"])
async def delete_app(
    payload: Annotated[DeleteAppPayload, Body()],
    crm_user: ResolvedCrmUser = Depends(resolve_user),
) -> dict[str, Any]:
    command = SdkAppCommandsMapper.delete_app_from_transport(GeneralMapper.transport_to_command_payload(crm_user, payload))
    return build_stub_response(command)


@router.get("/{app_id}/platform/{platform_id}", tags=["admin", "app"])
async def get_app_platform(
    app_id: int,
    platform_id: int,
    crm_user: ResolvedCrmUser = Depends(resolve_user),
) -> dict[str, Any]:
    command = SdkAppCommandsMapper.get_app_platform_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, app_id=app_id, platform_id=platform_id)
    )
    return build_stub_response(command)

@router.get("/{app_id}/platform", tags=["admin", "app"])
async def list_app_platforms(
    app_id: int,
    pagination_queries: Annotated[PaginationQueryPayload, Query()],
    crm_user: ResolvedCrmUser = Depends(resolve_user),
) -> dict[str, Any]:
    command = SdkAppCommandsMapper.list_app_platforms_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, pagination_queries, app_id=app_id)
    )
    return build_stub_response(command)


@router.patch("/{app_id}/platform/{platform_id}", tags=["admin", "app"])
async def update_app_platform(
    app_id: int,
    platform_id: int,
    payload: Annotated[UpdateAppPlatformPayload, Body()],
    crm_user: ResolvedCrmUser = Depends(resolve_user),
) -> dict[str, Any]:
    command = SdkAppCommandsMapper.update_app_platform_from_transport(
        GeneralMapper.transport_to_command_payload(
            crm_user,
            payload,
            app_id=app_id,
            platform_id=platform_id,
        )
    )
    return build_stub_response(command)


@router.post("/platform", status_code=status.HTTP_201_CREATED, tags=["admin", "app"])
async def create_app_platform(
    payload: Annotated[CreateAppPlatformPayload, Body()],
    crm_user: ResolvedCrmUser = Depends(resolve_user),
) -> dict[str, Any]:
    command = SdkAppCommandsMapper.create_app_platform_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, payload)
    )
    return build_stub_response(command)


@router.delete("/{app_id}/platform/{platform_id}", tags=["admin", "app"])
async def delete_app_platform(
    app_id: int,
    platform_id: int,
    crm_user: ResolvedCrmUser = Depends(resolve_user),
) -> dict[str, Any]:
    command = SdkAppCommandsMapper.delete_app_platform_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, app_id=app_id, platform_id=platform_id)
    )
    return build_stub_response(command)
