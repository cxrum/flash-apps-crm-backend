from __future__ import annotations

import pytest

from app.modules.analytics.application.s2s.exception import SignatureMismatch
from app.modules.analytics.application.s2s.service import ClickService
from app.modules.analytics.core.exception import AnalyticsApplicationException
from app.modules.crm.application.contracts.ip2location import IpLocation
from app.modules.crm.domain.app_platform.CrmAppPlatformEntity import CrmAppPlatformEntity
from app.modules.crm.domain.hash_protocol import HashableValue
from tests.unit.builders import (
    build_app_entity,
    build_app_platform_entity,
    build_click_entity,
    build_s2s_click_command,
    build_tracking_redirect_command,
)
from tests.unit.builders.entities import build_param_definition_entity
from tests.unit.doubles.application.ip2location import StubIP2LocationGateway
from tests.unit.doubles.application.signature import StubSignatureService
from tests.unit.doubles.domain.uow import StubUnitOfWork, StubUoWFactory


def _seed_platform(
    uow: StubUnitOfWork,
    *,
    app_id: int = 1,
    app_code: str = "test-app",
    platform: str = "ios",
) -> CrmAppPlatformEntity:
    uow.app_repo.save(build_app_entity(app_id=app_id, code_slug=app_code))
    return uow.app_platform_repo.save(
        build_app_platform_entity(
            app_id=app_id,
            platform=platform,
            install_key=f"{platform}-install-key",
        )
    )


def _build_service(
    uow: StubUnitOfWork,
    *,
    compare_result: bool | None = True,
) -> tuple[ClickService, StubSignatureService, StubIP2LocationGateway]:
    signature_service = StubSignatureService()
    signature_service.compare_result = compare_result

    ip2location_gateway = StubIP2LocationGateway()
    ip2location_gateway.seed(
        ip="203.0.113.10",
        location=IpLocation(
            city="Paris",
            country="France",
            country_code="FR",
            region="Ile-de-France",
            language="fr",
        ),
    )

    return (
        ClickService(StubUoWFactory(uow), signature_service, ip2location_gateway),
        signature_service,
        ip2location_gateway,
    )


def test_process_s2s_click_raises_for_unknown_app_code() -> None:
    service, signature_service, ip2location_gateway = _build_service(StubUnitOfWork())

    with pytest.raises(AnalyticsApplicationException) as error:
        service.process_s2s_click(build_s2s_click_command(app_code="missing-app"))

    assert error.value.message_key == "sdk.s2s.app_code.unknown"
    assert signature_service.calls == []
    assert ip2location_gateway.calls == []


def test_process_s2s_click_raises_for_unknown_platform() -> None:
    uow = StubUnitOfWork()
    service, _, _ = _build_service(uow)
    _seed_platform(uow, platform="ios")

    with pytest.raises(AnalyticsApplicationException) as error:
        service.process_s2s_click(build_s2s_click_command(platform="android"))

    assert error.value.message_key == "sdk.s2s.platform.not_configured"


def test_process_s2s_click_rejects_invalid_signature() -> None:
    uow = StubUnitOfWork()
    service, signature_service, ip2location_gateway = _build_service(uow, compare_result=False)
    platform = _seed_platform(uow)

    with pytest.raises(AnalyticsApplicationException):
        service.process_s2s_click(
            build_s2s_click_command(
                app_code="test-app",
                platform=platform.platform,
            )
        )

    assert [call.method for call in signature_service.calls] == ["compare"]
    assert signature_service.calls[0].args == (
        HashableValue.from_str("campaign=spring"),
        HashableValue.from_hex("746573742d7369676e6174757265"),
        HashableValue.from_str(platform.sdk_secret_encrypted),
    )
    assert ip2location_gateway.calls == []


def test_process_s2s_click_rejects_malformed_signature_without_external_work() -> None:
    uow = StubUnitOfWork()
    service, signature_service, ip2location_gateway = _build_service(uow)
    platform = _seed_platform(uow)

    with pytest.raises(SignatureMismatch) as error:
        service.process_s2s_click(
            build_s2s_click_command(
                platform=platform.platform,
                signature="not-hex",
            )
        )

    assert error.value.code == 401
    assert signature_service.calls == []
    assert ip2location_gateway.calls == []
    assert uow.click_repo.list_by_platform_id(platform.platform_id or 0) == []


def test_process_s2s_click_accepts_missing_source_without_location_lookup() -> None:
    uow = StubUnitOfWork()
    service, signature_service, ip2location_gateway = _build_service(uow)
    platform = _seed_platform(uow)
    uow.param_definition_repo.save(build_param_definition_entity())
    command = build_s2s_click_command(
        click_id="expired-source-click",
        ip=None,
        params={"utm_source": "partner"},
    )

    response = service.process_s2s_click(command)
    saved_click = uow.click_repo.get_by_id(response.click_id)

    assert saved_click is not None
    assert saved_click.status == "accepted"
    assert saved_click.normalized_params == {"utm_source": "partner"}
    assert saved_click.city is None
    assert signature_service.calls[0].args == (
        HashableValue.from_str("utm_source=partner"),
        HashableValue.from_hex(command.signature),
        HashableValue.from_str(platform.sdk_secret_encrypted),
    )
    assert ip2location_gateway.calls == []


def test_process_s2s_click_inserts_duplicate_click_with_s2s_metadata() -> None:
    uow = StubUnitOfWork()
    service, signature_service, ip2location_gateway = _build_service(uow)
    platform = _seed_platform(uow)

    uow.param_definition_repo.save(build_param_definition_entity())

    existing_click = uow.click_repo.insert(
        build_click_entity(
            click_id="partner-click-1",
            app_platform_id=platform.platform_id or 0,
        )
    )

    response = service.process_s2s_click(
        build_s2s_click_command(
            click_id="partner-click-1",
            params={"utm_source": "anton", "campaign": "spring"},
            ip="203.0.113.10",
            user_agent="PartnerBot/1.0",
            redirect_url="https://example.com/landing",
        )
    )

    saved_click = uow.click_repo.get_by_id(response.click_id)

    assert response.click_id != existing_click.click_id
    assert saved_click is not None
    assert saved_click.app_platform_id == platform.platform_id
    assert saved_click.raw_query == {"campaign": "spring", "utm_source": "anton"}
    assert saved_click.normalized_params == {"utm_source": "anton"}
    assert saved_click.redirect_target == "https://example.com/landing"
    assert saved_click.city == "Paris"
    assert saved_click.country_code == "FR"
    assert saved_click.language == "fr"
    assert saved_click.region == "Ile-de-France"
    assert saved_click.status == "duplicate"
    assert [call.method for call in signature_service.calls] == ["compare"]
    assert signature_service.calls[0].args[0] == HashableValue.from_str("campaign=spring&utm_source=anton")
    assert [call.method for call in ip2location_gateway.calls] == ["resolve"]


def test_process_redirect_click_creates_accepted_click_with_location_metadata() -> None:
    uow = StubUnitOfWork()
    service, _, ip2location_gateway = _build_service(uow)
    platform = _seed_platform(uow)

    uow.param_definition_repo.save(build_param_definition_entity())

    response = service.process_redirect_click(
        build_tracking_redirect_command(
            app_code="test-app",
            platform=platform.platform,
            ip="203.0.113.10",
            params={"campaign": "spring", "utm_source": "anton"},
        )
    )

    saved_click = uow.click_repo.get_by_id(response.click_id)

    assert saved_click is not None
    assert saved_click.status == "accepted"
    assert saved_click.app_platform_id == platform.platform_id
    assert saved_click.normalized_params == {"utm_source": "anton"}
    assert saved_click.city == "Paris"
    assert saved_click.country_code == "FR"
    assert [call.method for call in ip2location_gateway.calls] == ["resolve"]
