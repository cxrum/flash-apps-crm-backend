from typing import Annotated

from fastapi import APIRouter, Body, Depends, Query, status

from app.api.v1.crm.payloads import (
    CreateAppPayload,
    CreateAppPlatformPayload,
    DeleteAppPayload,
    UpdateAppPayload,
    UpdateAppPlatformPayload,
)
from app.api.v1.transport import PaginationQueryPayload
from app.application.base import JsonDict
from app.application.crm_authentication.responses import ResolvedCrmUserResponse
from app.application.sdk.apps.mappers import SdkAppCommandsMapper
from app.application.sdk.apps.protocol import AppServiceProtocol
from app.core.utils.general_mapper import GeneralMapper
from app.di.dependencies import resolve_user
from app.di.services import get_sdk_app_service

router = APIRouter()


@router.get("/{app_id}", tags=["admin", "app"])
async def get_app(
    app_id: int,
    crm_user: ResolvedCrmUserResponse = Depends(resolve_user),
    app_service: AppServiceProtocol = Depends(get_sdk_app_service),
) -> JsonDict:
    command = SdkAppCommandsMapper.get_app_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, app_id=app_id)
    )

    response = app_service.get_app(command)
    return response.model_dump(mode="json")


@router.get("/", tags=["admin", "app"])
async def list_apps(
    pagination_queries: Annotated[PaginationQueryPayload, Query()],
    crm_user: ResolvedCrmUserResponse = Depends(resolve_user),
    app_service: AppServiceProtocol = Depends(get_sdk_app_service),
) -> JsonDict:
    command = SdkAppCommandsMapper.list_apps_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, pagination_queries)
    )

    response = app_service.get_apps(command)

    return response.model_dump(mode="json")


@router.post("/", status_code=status.HTTP_201_CREATED, tags=["admin", "app"])
async def create_app(
    payload: Annotated[CreateAppPayload, Body()],
    crm_user: ResolvedCrmUserResponse = Depends(resolve_user),
    app_service: AppServiceProtocol = Depends(get_sdk_app_service),
) -> JsonDict:
    command = SdkAppCommandsMapper.create_app_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, payload)
    )

    response = app_service.create_app(command)

    return response.model_dump(mode="json")


@router.patch("/", status_code=status.HTTP_201_CREATED, tags=["admin", "app"])
async def update_app(
    payload: Annotated[UpdateAppPayload, Body()],
    crm_user: ResolvedCrmUserResponse = Depends(resolve_user),
    app_service: AppServiceProtocol = Depends(get_sdk_app_service),
) -> JsonDict:
    command = SdkAppCommandsMapper.update_app_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, payload)
    )

    response = app_service.update_app(command)

    return response.model_dump(mode="json")


@router.delete("/", status_code=status.HTTP_201_CREATED, tags=["admin", "app"])
async def delete_app(
    payload: Annotated[DeleteAppPayload, Body()],
    crm_user: ResolvedCrmUserResponse = Depends(resolve_user),
    app_service: AppServiceProtocol = Depends(get_sdk_app_service),
) -> JsonDict:

    command = SdkAppCommandsMapper.delete_app_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, payload)
    )

    response = app_service.delete_app(command)

    return response.model_dump(mode="json")


@router.get("/{app_id}/platform/{platform_id}", tags=["admin", "app"])
async def get_app_platform(
    app_id: int,
    platform_id: int,
    crm_user: ResolvedCrmUserResponse = Depends(resolve_user),
    app_service: AppServiceProtocol = Depends(get_sdk_app_service),
) -> JsonDict:
    command = SdkAppCommandsMapper.get_app_platform_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, app_id=app_id, platform_id=platform_id)
    )

    response = app_service.get_app_platform(command)

    return response.model_dump(mode="json")


@router.get("/{app_id}/platform", tags=["admin", "app"])
async def list_app_platforms(
    app_id: int,
    pagination_queries: Annotated[PaginationQueryPayload, Query()],
    crm_user: ResolvedCrmUserResponse = Depends(resolve_user),
    app_service: AppServiceProtocol = Depends(get_sdk_app_service),
) -> JsonDict:
    command = SdkAppCommandsMapper.list_app_platforms_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, pagination_queries, app_id=app_id)
    )

    response = app_service.get_app_platforms(command)

    return response.model_dump(mode="json")


@router.patch("/{app_id}/platform/{platform_id}", tags=["admin", "app"])
async def update_app_platform(
    app_id: int,
    platform_id: int,
    payload: Annotated[UpdateAppPlatformPayload, Body()],
    crm_user: ResolvedCrmUserResponse = Depends(resolve_user),
    app_service: AppServiceProtocol = Depends(get_sdk_app_service),
) -> JsonDict:
    command = SdkAppCommandsMapper.update_app_platform_from_transport(
        GeneralMapper.transport_to_command_payload(
            crm_user,
            payload,
            app_id=app_id,
            platform_id=platform_id,
        )
    )

    response = app_service.update_app_platform(command)

    return response.model_dump(mode="json")


@router.post("/platform", status_code=status.HTTP_201_CREATED, tags=["admin", "app"])
async def create_app_platform(
    payload: Annotated[CreateAppPlatformPayload, Body()],
    crm_user: ResolvedCrmUserResponse = Depends(resolve_user),
    app_service: AppServiceProtocol = Depends(get_sdk_app_service),
) -> JsonDict:
    command = SdkAppCommandsMapper.create_app_platform_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, payload)
    )

    response = app_service.create_app_platform(command)

    return response.model_dump(mode="json")


@router.delete("/{app_id}/platform/{platform_id}", tags=["admin", "app"])
async def delete_app_platform(
    app_id: int,
    platform_id: int,
    crm_user: ResolvedCrmUserResponse = Depends(resolve_user),
    app_service: AppServiceProtocol = Depends(get_sdk_app_service),
) -> JsonDict:
    command = SdkAppCommandsMapper.delete_app_platform_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, app_id=app_id, platform_id=platform_id)
    )

    response = app_service.delete_app_platform(command)

    return response.model_dump(mode="json")


@router.post(
    "/{app_id}/platform/{platform_id}/rotate",
    tags=["admin", "app", "secrets"],
)
async def rotate_platform_secret(
    app_id: int,
    platform_id: int,
    crm_user: ResolvedCrmUserResponse = Depends(resolve_user),
    app_service: AppServiceProtocol = Depends(get_sdk_app_service),
) -> JsonDict:
    command = SdkAppCommandsMapper.rotate_platform_secret_from_transport(
        GeneralMapper.transport_to_command_payload(crm_user, app_id=app_id, platform_id=platform_id)
    )

    response = app_service.rotate_platform_secret(command)

    return response.model_dump(mode="json")
