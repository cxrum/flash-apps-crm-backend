from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Body, Depends, Query, Response, status

from app.modules.analytics.api.v1.ingestion.payloads import (
    SdkEventsPayload,
    SdkInstallPayload,
    SdkParamsUpdatePayload,
)
from app.modules.analytics.application.ingestion.mappers import SdkIngestionCommandMapper
from app.modules.analytics.application.ingestion.protocol import IngestionServiceProtocol
from app.modules.analytics.di.services import get_analytics_ingestion_service
from app.modules.crm.application.sdk.apps.protocol import AppServiceProtocol
from app.modules.crm.core.utils.general_mapper import GeneralMapper
from app.modules.crm.di.services import get_sdk_app_service

router = APIRouter()


@router.post("/install", status_code=status.HTTP_202_ACCEPTED, tags=["sdk"])
async def create_or_link_install(
    payload: Annotated[SdkInstallPayload, Body()],
    ingestion_service: IngestionServiceProtocol = Depends(get_analytics_ingestion_service),
) -> str:
    command = SdkIngestionCommandMapper.install_from_transport(GeneralMapper.to_dict(payload))
    response = await ingestion_service.process_install(command)
    return response.model_dump_json()


@router.post("/events", status_code=status.HTTP_202_ACCEPTED, tags=["sdk"])
async def ingest_sdk_events(
    payload: Annotated[SdkEventsPayload, Body()],
    ingestion_service: IngestionServiceProtocol = Depends(get_analytics_ingestion_service),
) -> Response:
    command = SdkIngestionCommandMapper.events_from_transport(GeneralMapper.to_dict(payload))
    await ingestion_service.process_batch_events(command)
    return Response(status_code=status.HTTP_202_ACCEPTED)


@router.post("/params/update", status_code=status.HTTP_202_ACCEPTED, tags=["sdk"])
async def update_sdk_params(
    payload: Annotated[SdkParamsUpdatePayload, Body()],
    ingestion_service: IngestionServiceProtocol = Depends(get_analytics_ingestion_service),
) -> Response:
    command = SdkIngestionCommandMapper.params_update_from_transport(GeneralMapper.to_dict(payload))
    await ingestion_service.update_params(command)
    return Response(status_code=status.HTTP_202_ACCEPTED)


@router.get("/config", tags=["sdk"])
async def get_public_config(
    install_key: Annotated[str | None, Query()] = None,
    app_service: AppServiceProtocol = Depends(get_sdk_app_service),
) -> str:
    command = SdkIngestionCommandMapper.config_from_transport(GeneralMapper.to_dict(install_key=install_key))
    response = app_service.get_app_config_secrets(command)
    return response.model_dump_json()
