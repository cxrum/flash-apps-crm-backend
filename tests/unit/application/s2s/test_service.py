from __future__ import annotations

import pytest

from app.application.exceptions import ApplicationError
from app.application.s2s.servicie import S2SService
from app.domain.app_platform.CrmAppPlatformEntity import CrmAppPlatformEntity
from tests.unit.builders import (
    build_app_entity,
    build_app_platform_entity,
    build_click_entity,
    build_s2s_click_command,
)
from tests.unit.doubles.domain.uow import StubUnitOfWork


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


def test_process_click_raises_for_unknown_app_code() -> None:
    service = S2SService(StubUnitOfWork())

    with pytest.raises(ApplicationError, match="Unknown app code"):
        service.process_click(build_s2s_click_command(app_code="missing-app"))


def test_process_click_raises_for_unknown_platform() -> None:
    uow = StubUnitOfWork()
    service = S2SService(uow)
    _seed_platform(uow, platform="ios")

    with pytest.raises(ApplicationError, match="is not configured"):
        service.process_click(build_s2s_click_command(platform="android"))


def test_process_click_inserts_click_with_s2s_metadata() -> None:
    uow = StubUnitOfWork()
    service = S2SService(uow)
    platform = _seed_platform(uow)

    response = service.process_click(
        build_s2s_click_command(
            click_id="partner-click-1",
            params={"campaign": "spring"},
            ip="203.0.113.10",
            user_agent="PartnerBot/1.0",
            redirect_url="https://example.com/landing",
        )
    )
    saved_click = uow.click_repo.get_by_id(response.click_id)

    assert response.click_id == "partner-click-1"
    assert saved_click is not None
    assert saved_click.app_platform_id == platform.platform_id
    assert saved_click.source == "s2s"
    assert saved_click.raw_query == {"campaign": "spring"}
    assert saved_click.redirect_target == "https://example.com/landing"


def test_process_click_returns_existing_click_for_idempotent_retry() -> None:
    uow = StubUnitOfWork()
    service = S2SService(uow)
    platform = _seed_platform(uow)
    existing_click = uow.click_repo.insert(
        build_click_entity(
            click_id="partner-click-1",
            app_platform_id=platform.platform_id or 0,
            source="s2s",
        )
    )

    response = service.process_click(build_s2s_click_command(click_id=existing_click.click_id))
    platform_clicks = uow.click_repo.list_by_platform_id(platform.platform_id or 0)

    assert response.click_id == existing_click.click_id
    assert [click.click_id for click in platform_clicks] == ["partner-click-1"]
