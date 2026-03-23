from __future__ import annotations

import asyncio

import pytest
from fastapi import HTTPException, Response

from app.api.v1.crm.admin import (
    create_app,
    create_app_platform,
    create_postback,
    list_apps,
)
from app.api.v1.crm.payloads import (
    CreateAppPayload,
    CreateAppPlatformPayload,
    CreatePostbackRulePayload,
)
from app.application.sdk.usecases.apps.responses import CreateAppResponse, CreatePlatformResponse


class StubAppService:
    def __init__(self) -> None:
        self.create_app_commands = []
        self.create_platform_commands = []

    def create_app(self, command):
        self.create_app_commands.append(command)
        return CreateAppResponse(app_id=42)

    def create_platform(self, command):
        self.create_platform_commands.append(command)
        return CreatePlatformResponse(platform_id=7)


class StubPostbackService:
    def __init__(self) -> None:
        self.create_rule_commands = []

    def create_rule(self, command) -> None:
        self.create_rule_commands.append(command)


def test_create_app_uses_application_service_with_compatible_payload() -> None:
    async def scenario() -> None:
        service = StubAppService()

        response = await create_app(
            CreateAppPayload(
                id=1,
                code="test-app",
                name="Test App",
                description="Admin managed application",
                screanshots={"0": "https://cdn.example.com/shot-1.png"},
                tech_description="Technical description",
                logo_ur="https://cdn.example.com/logo.png",
            ),
            app_service=service,
        )

        assert response == {"app_id": 42}
        assert len(service.create_app_commands) == 1
        command = service.create_app_commands[0]
        assert command.id == 1
        assert command.code_slug == "test-app"
        assert command.screanshots == {"0": "https://cdn.example.com/shot-1.png"}
        assert command.tech_description == "Technical description"

    asyncio.run(scenario())


def test_create_app_reports_payload_contract_gap_when_id_is_missing() -> None:
    async def scenario() -> None:
        with pytest.raises(HTTPException, match="requires an `id` field"):
            await create_app(
                CreateAppPayload(
                    code="test-app",
                    name="Test App",
                    description="Admin managed application",
                ),
                app_service=StubAppService(),
            )

    asyncio.run(scenario())


def test_create_app_platform_uses_application_service_with_compatible_payload() -> None:
    async def scenario() -> None:
        service = StubAppService()

        response = await create_app_platform(
            1,
            CreateAppPlatformPayload(
                platform="ios",
                install_key="install-key-ios",
                is_active=False,
                package_name="com.example.test",
                store_url="https://apps.example.com/test",
                sdk_public_key="sdk-public",
                sdk_secret_hash="sdk-secret-hash",
            ),
            app_service=service,
        )

        assert response == {"platform_id": 7}
        assert len(service.create_platform_commands) == 1
        command = service.create_platform_commands[0]
        assert command.app_id == 1
        assert command.platform == "ios"
        assert command.package_name == "com.example.test"
        assert command.status == "inactive"

    asyncio.run(scenario())


def test_create_postback_uses_application_service_when_full_command_shape_is_present() -> None:
    async def scenario() -> None:
        service = StubPostbackService()

        response = await create_postback(
            CreatePostbackRulePayload(
                app_id=1,
                name="Install Rule",
                url="https://example.com/postback",
                is_active=True,
                trigger_type="install",
                http_method="POST",
                headers={},
                auth_params={},
                timeout=30,
                retry_policy={},
                tempalte={},
            ),
            postback_service=service,
        )

        assert isinstance(response, Response)
        assert response.status_code == 201
        assert len(service.create_rule_commands) == 1
        command = service.create_rule_commands[0]
        assert command.app_id == 1
        assert command.name == "Install Rule"
        assert command.trigger_type == "install"
        assert command.http_method == "POST"

    asyncio.run(scenario())


def test_list_apps_reports_missing_application_service() -> None:
    async def scenario() -> None:
        with pytest.raises(HTTPException, match="does not expose a listing service"):
            await list_apps(limit=50, offset=0, search=None)

    asyncio.run(scenario())
