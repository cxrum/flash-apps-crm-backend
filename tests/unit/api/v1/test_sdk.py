from __future__ import annotations

import asyncio

import pytest
from fastapi import FastAPI
from fastapi import HTTPException, Response

from app.api.v1.sdk.payloads import (
    SdkDevicePayload,
    SdkEventPayload,
    SdkEventsPayload,
    SdkInstallPayload,
    SdkParamsUpdatePayload,
    SdkPushRegisterPayload,
)
from app.api.v1.sdk.sdk import (
    create_or_link_install,
    get_public_config,
    ingest_sdk_events,
    register_push_token,
    router,
    update_sdk_params,
)
from app.application.sdk.usecases.ingestion.responses import SdkInstallResponse


class StubIngestionService:
    def __init__(self) -> None:
        self.install_commands = []
        self.events_commands = []
        self.params_commands = []

    async def process_install(self, command):
        self.install_commands.append(command)
        return SdkInstallResponse(click_id="click-transport", app_user_id=7)

    async def process_batch_events(self, command):
        self.events_commands.append(command)
        return None

    async def udate_params(self, command):
        self.params_commands.append(command)
        return None


def build_device_payload() -> SdkDevicePayload:
    return SdkDevicePayload(
        os_name="iOS",
        os_version="17.4",
        device_brand="Apple",
        device_model="iPhone 15",
        app_version="1.0.0",
        sdk_version="2.1.0",
    )


def test_create_or_link_install_calls_ingestion_service_and_returns_transport_payload() -> None:
    async def scenario() -> None:
        service = StubIngestionService()

        response = await create_or_link_install(
            SdkInstallPayload(
                install_key="install-key-ios",
                idempotency_key="install-1",
                click_id="click-1",
                params={"utm_source": "organic"},
                device=build_device_payload(),
            ),
            ingestion_service=service,
        )

        assert response == {
            "click_id": "click-transport",
            "app_user_id": 7,
        }
        assert len(service.install_commands) == 1
        assert service.install_commands[0].install_key == "install-key-ios"
        assert service.install_commands[0].device.sdk_version == "2.1.0"

    asyncio.run(scenario())


def test_ingest_sdk_events_calls_ingestion_service_and_returns_accepted_response() -> None:
    async def scenario() -> None:
        service = StubIngestionService()

        response = await ingest_sdk_events(
            SdkEventsPayload(
                install_key="install-key-ios",
                click_id="click-1",
                idempotency_key="batch-1",
                events=[
                    SdkEventPayload(
                        idempotency_key="event-1",
                        type="metric",
                        key="first_open",
                        params={"source": "sdk"},
                    )
                ],
            ),
            ingestion_service=service,
        )

        assert isinstance(response, Response)
        assert response.status_code == 202
        assert len(service.events_commands) == 1
        assert service.events_commands[0].click_id == "click-1"
        assert service.events_commands[0].events[0].key == "first_open"

    asyncio.run(scenario())


def test_update_sdk_params_calls_ingestion_service_and_returns_accepted_response() -> None:
    async def scenario() -> None:
        service = StubIngestionService()

        response = await update_sdk_params(
            SdkParamsUpdatePayload(
                click_id="click-1",
                idempotency_key="params-1",
                params={"campaign": "spring"},
            ),
            ingestion_service=service,
        )

        assert isinstance(response, Response)
        assert response.status_code == 202
        assert len(service.params_commands) == 1
        assert service.params_commands[0].click_id == "click-1"
        assert service.params_commands[0].params == {"campaign": "spring"}

    asyncio.run(scenario())


def test_register_push_token_reports_missing_application_service() -> None:
    async def scenario() -> None:
        with pytest.raises(HTTPException, match="application layer service is missing"):
            await register_push_token(
                SdkPushRegisterPayload(
                    install_key="install-key-ios",
                    token="push-token-1",
                    provider="apns",
                )
            )

    asyncio.run(scenario())


def test_get_public_config_reports_incompatible_application_service_contract() -> None:
    async def scenario() -> None:
        with pytest.raises(HTTPException, match="application service contract is incompatible"):
            await get_public_config(
                install_key="install-key-ios",
                app_code=None,
                platform="ios",
                crm_user_id=None,
            )

    asyncio.run(scenario())


def test_sdk_openapi_contains_examples_derived_from_service_tests() -> None:
    app = FastAPI()
    app.include_router(router, prefix="/api/v1/sdk")

    schema = app.openapi()

    install_examples = (
        schema["paths"]["/api/v1/sdk/install"]["post"]["requestBody"]["content"]["application/json"]["examples"]
    )
    assert install_examples["first_install"]["value"]["install_key"] == "install-key-ios"
    assert install_examples["link_existing_click"]["value"]["click_id"] == "redirect-click-1"

    event_examples = (
        schema["paths"]["/api/v1/sdk/events"]["post"]["requestBody"]["content"]["application/json"]["examples"]
    )
    assert event_examples["mixed_batch"]["value"]["events"][1]["currency"] == "EUR"
    assert event_examples["mixed_batch"]["value"]["events"][1]["amount"] == 5.0

    params_examples = (
        schema["paths"]["/api/v1/sdk/params/update"]["post"]["requestBody"]["content"]["application/json"]["examples"]
    )
    assert params_examples["campaign_snapshot"]["value"]["params"]["campaign"] == "spring-launch"

    push_response_example = (
        schema["paths"]["/api/v1/sdk/push/register"]["post"]["responses"]["501"]["content"]["application/json"]["example"]
    )
    assert "application layer service is missing" in push_response_example["detail"]

    config_response_example = (
        schema["paths"]["/api/v1/sdk/config"]["get"]["responses"]["501"]["content"]["application/json"]["example"]
    )
    assert "application service contract is incompatible" in config_response_example["detail"]
