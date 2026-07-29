from __future__ import annotations

import asyncio
from datetime import UTC, date, datetime
from urllib.parse import urlencode

import pytest

from app.modules.crm.application.admin.postback.service import PostbackService
from app.modules.crm.application.exception import GeneralException
from app.modules.crm.domain.app.CrmAppEntity import CrmAppEntity
from app.modules.crm.domain.app_platform.CrmAppPlatformEntity import CrmAppPlatformEntity
from app.modules.crm.domain.click.CrmClickEntity import CrmClickEntity
from app.modules.crm.domain.current_param.CrmCurrentParamEntity import CrmCurrentParamEntity
from app.modules.crm.domain.event_bus.service_protocol import IAsyncEventBus
from app.modules.crm.domain.events.CrmEventEntity import EventEntity
from app.modules.crm.domain.exceptions import DomainException
from app.modules.crm.domain.install.CrmInstallEntity import CrmInstallEntity
from app.modules.crm.domain.postback_rule.CrmPostbackRuleEntity import CrmPostbackRuleEntity
from app.modules.crm.domain.postback_rule.template import PostbackTemplateEntity
from app.modules.crm.domain.secret_template.CrmSecretTemplateEntity import CrmSecretTemplateEntity
from tests.unit.builders import (
    build_admin_create_postback_rule_command,
    build_admin_evaluate_postback_rule_command,
    build_admin_execute_postback_rule_command,
    build_app_entity,
    build_app_platform_entity,
    build_app_secret_entity,
    build_click_entity,
    build_current_param_entity,
    build_event_entity,
    build_install_entity,
    build_param_definition_entity,
    build_postback_rule_entity,
    build_secret_template_entity,
)
from tests.unit.doubles.application import StubS2SRequester
from tests.unit.doubles.domain.uow import StubUnitOfWork, StubUoWFactory


class _AllowPostbackAuthorization:
    def required_user_permission(self, **_: object) -> None:
        return None


def _seed_platform(
    uow: StubUnitOfWork,
    *,
    app_id: int = 1,
    platform: str = "ios",
    install_key: str | None = None,
) -> CrmAppPlatformEntity:
    return uow.app_platform_repo.save(
        build_app_platform_entity(
            app_id=app_id,
            platform=platform,
            install_key=install_key or f"{platform}-install-key",
        )
    )


def _seed_event_context(
    uow: StubUnitOfWork,
    *,
    app_id: int = 1,
    app_code: str = "test-app",
    platform: str = "ios",
    click_id: str = "click-1",
    event_id: str = "evt-1",
    event_type: str = "conversion",
    event_key: str = "purchase",
    payload: dict[str, object] | None = None,
    app_user_id: int = 77,
) -> tuple[CrmAppEntity, CrmAppPlatformEntity, CrmClickEntity, CrmInstallEntity, EventEntity]:
    app = uow.app_repo.save(build_app_entity(app_id=app_id, code_slug=app_code))
    platform_entity = _seed_platform(uow, app_id=app_id, platform=platform)
    click = uow.click_repo.insert(
        build_click_entity(
            click_id=click_id,
            app_platform_id=platform_entity.platform_id or 0,
        )
    )
    install = uow.install_repo.save(
        build_install_entity(
            click_id=click.click_id,
            app_platform_id=platform_entity.platform_id or 0,
            app_user_id=app_user_id,
        )
    )
    event = uow.event_repo.insert(
        build_event_entity(
            event_id=event_id,
            click_id=click.click_id,
            event_type=event_type,
            event_key=event_key,
            amount=12.5,
            amount_usd=10.0,
            payload=payload
            or {
                "campaign": "spring",
                "geo": "US",
                "ip": "203.0.113.10",
                "ua": "PartnerBot/1.0",
            },
        )
    )
    return app, platform_entity, click, install, event


def _seed_secret(
    uow: StubUnitOfWork,
    *,
    platform_id: int,
    code: str = "api_key",
    encrypted_value: str = "enc::api-key-v1",
    version: float = 1.0,
    active_flag: bool = True,
) -> CrmSecretTemplateEntity:
    template = uow.secret_template_repo.save(build_secret_template_entity(code=code))
    assert template.template_id is not None
    uow.app_secret_repo.save(
        build_app_secret_entity(
            template_id=template.template_id,
            platform_id=platform_id,
            encrypted_value=encrypted_value,
            version=version,
            active_flag=active_flag,
        )
    )
    return template


def _build_service(
    uow: StubUnitOfWork,
    async_event_bus: IAsyncEventBus,
) -> tuple[PostbackService, StubS2SRequester]:
    requester = StubS2SRequester()
    service = PostbackService(
        StubUoWFactory(uow),
        async_event_bus,
        requester,
        authorization_service=_AllowPostbackAuthorization(),
    )
    return service, requester


def _assert_saved_rule(
    rule: CrmPostbackRuleEntity,
    *,
    platform_id: int,
) -> None:
    assert rule.platform_app_id == platform_id
    assert rule.name == "Conversion Rule"
    assert rule.endpoint_url == "https://example.com/postback/conversion"
    assert rule.trigger_type == "conversion"
    assert rule.http_method == "GET"
    assert rule.headers == {"X-Test": "postback"}
    assert rule.event_key == "purchase"
    assert rule.auth_params == {"Authorization": "api_key"}
    assert rule.timeout == 45
    assert rule.retry_policy == {"attempts": 3}
    assert dict(rule.template.items()) == {
        "click_id": "{click_id}",
        "campaign": "{current.utm_source}",
    }
    assert rule.is_active is False
    assert rule.rule_id is not None


CURRENT_PARAM_TYPE_CASES = [
    pytest.param("string", {"value_string": "organic"}, "organic", id="string"),
    pytest.param("integer", {"value_number": 42.0, "value_string": None}, 42, id="integer"),
    pytest.param("float", {"value_number": 42.5, "value_string": None}, 42.5, id="float"),
    pytest.param("boolean", {"value_bool": True, "value_string": None}, True, id="boolean"),
    pytest.param("date", {"value_string": "2026-03-13"}, date(2026, 3, 13), id="date"),
    pytest.param(
        "datetime",
        {"value_string": "2026-03-13T10:30:00Z"},
        datetime(2026, 3, 13, 10, 30, tzinfo=UTC),
        id="datetime",
    ),
    pytest.param("enum", {"value_string": "partner"}, "partner", id="enum"),
    pytest.param(
        "json",
        {
            "value_json": {"country": "US", "active": True},
            "value_string": None,
        },
        {"country": "US", "active": True},
        id="json",
    ),
    pytest.param(
        "list",
        {"value_json": ["email", "push"], "value_string": None},
        ["email", "push"],
        id="list",
    ),
]


def _seed_typed_current_param(
    uow: StubUnitOfWork,
    *,
    app_id: int,
    click_id: str,
    machine_key: str,
    data_type: str,
    current_value_kwargs: dict[str, object],
) -> None:
    uow.param_definition_repo.save(
        build_param_definition_entity(
            app_id=app_id,
            machine_key=machine_key,
            data_type=data_type,
        )
    )
    uow.current_param_repo.save(
        build_current_param_entity(
            click_id=click_id,
            param_key=machine_key,
            **current_value_kwargs,
        )
    )


def _build_expected_final_url(url: str, params: dict[str, object], *, http_method: str) -> str:
    if http_method != "GET" or not params:
        return url

    separator = "&" if "?" in url else "?"
    return f"{url}{separator}{urlencode(params, doseq=True)}"


def test_create_rule_creates_rules_for_all_app_platforms(
    async_event_bus: IAsyncEventBus,
) -> None:
    uow = StubUnitOfWork()
    service, _ = _build_service(uow, async_event_bus)
    ios = _seed_platform(uow, app_id=1, platform="ios")
    android = _seed_platform(uow, app_id=1, platform="android")
    _seed_platform(uow, app_id=2, platform="ios", install_key="other-ios-install-key")
    uow.secret_template_repo.save(build_secret_template_entity(code="api_key"))
    uow.app_platform_repo.reset_calls()

    service.create_postback(
        build_admin_create_postback_rule_command(
            app_id=1,
            name="Conversion Rule",
            trigger_type="conversion",
            event_key="purchase",
            url="https://example.com/postback/conversion",
            http_method="GET",
            headers={"X-Test": "postback"},
            auth_params={"Authorization": "api_key"},
            timeout=45,
            retry_policy={"attempts": 3},
            is_active=False,
            template={
                "click_id": "{click_id}",
                "campaign": "{current.utm_source}",
            },
        )
    )

    assert [call.method for call in uow.app_platform_repo.calls] == ["list_by_app_id"]

    saved_rules = uow.postback_rule_repo.list_by_app_id(1)

    assert [rule.platform_app_id for rule in saved_rules] == [ios.platform_id, android.platform_id]
    assert len(uow.postback_rule_repo.list_by_app_id(2)) == 0
    # Permission authorization runs in its own, read-only UoW before creation.
    assert uow.commit_count == 2
    assert uow.rollback_count == 0

    _assert_saved_rule(saved_rules[0], platform_id=ios.platform_id or 0)
    _assert_saved_rule(saved_rules[1], platform_id=android.platform_id or 0)


def test_create_rule_creates_rule_for_selected_platform_only(
    async_event_bus: IAsyncEventBus,
) -> None:
    uow = StubUnitOfWork()
    service, _ = _build_service(uow, async_event_bus)
    _seed_platform(uow, app_id=1, platform="ios")
    android = _seed_platform(uow, app_id=1, platform="android")
    uow.app_platform_repo.reset_calls()

    service.create_postback(
        build_admin_create_postback_rule_command(
            app_id=1,
            platform_app_id=android.platform_id,
        )
    )

    assert [call.method for call in uow.app_platform_repo.calls] == ["get_by_id"]

    saved_rules = uow.postback_rule_repo.list_by_app_id(1)

    assert len(saved_rules) == 1
    assert saved_rules[0].platform_app_id == android.platform_id
    assert saved_rules[0].name == "Install Rule"
    assert saved_rules[0].trigger_type == "install"
    assert uow.commit_count == 2
    assert uow.rollback_count == 0


def test_create_rule_raises_when_app_has_no_platforms(
    async_event_bus: IAsyncEventBus,
) -> None:
    uow = StubUnitOfWork()
    service, _ = _build_service(uow, async_event_bus)

    with pytest.raises(GeneralException):
        service.create_postback(build_admin_create_postback_rule_command(app_id=1))

    assert uow.commit_count == 1
    assert uow.rollback_count == 1
    assert uow.postback_rule_repo.list_by_app_id(1) == []


def test_create_rule_raises_when_selected_platform_does_not_exist(
    async_event_bus: IAsyncEventBus,
) -> None:
    uow = StubUnitOfWork()
    service, _ = _build_service(uow, async_event_bus)

    with pytest.raises(GeneralException, match="Platform doesn't exist"):
        service.create_postback(
            build_admin_create_postback_rule_command(
                app_id=1,
                platform_app_id=999,
            )
        )

    assert uow.commit_count == 1
    assert uow.rollback_count == 1


def test_create_rule_raises_for_unknown_secret_template(
    async_event_bus: IAsyncEventBus,
) -> None:
    uow = StubUnitOfWork()
    service, _ = _build_service(uow, async_event_bus)
    _seed_platform(uow)

    with pytest.raises(DomainException, match="Secret template: missing-secret"):
        service.create_postback(
            build_admin_create_postback_rule_command(
                auth_params={"Authorization": "missing-secret"},
            )
        )

    assert uow.commit_count == 1
    assert uow.rollback_count == 1


def test_create_rule_raises_for_invalid_template_placeholder(
    async_event_bus: IAsyncEventBus,
) -> None:
    uow = StubUnitOfWork()
    service, _ = _build_service(uow, async_event_bus)
    _seed_platform(uow)

    with pytest.raises(DomainException):
        service.create_postback(
            build_admin_create_postback_rule_command(
                template={"campaign": "current.utm_source"},
            )
        )

    assert uow.commit_count == 1
    assert uow.rollback_count == 1


def test_evaluate_raises_when_event_does_not_exist(
    async_event_bus: IAsyncEventBus,
) -> None:
    uow = StubUnitOfWork()
    service, _ = _build_service(uow, async_event_bus)

    with pytest.raises(GeneralException):
        service.evaluate(build_admin_evaluate_postback_rule_command(event_id="missing-event"))

    assert uow.commit_count == 0
    assert uow.rollback_count == 1


def test_evaluate_raises_when_click_does_not_exist(
    async_event_bus: IAsyncEventBus,
) -> None:
    uow = StubUnitOfWork()
    service, _ = _build_service(uow, async_event_bus)
    uow.event_repo.insert(build_event_entity(event_id="evt-1", click_id="missing-click"))

    with pytest.raises(GeneralException):
        service.evaluate(build_admin_evaluate_postback_rule_command())

    assert uow.commit_count == 0
    assert uow.rollback_count == 1


def test_evaluate_returns_only_rules_matching_platform_and_trigger(
    async_event_bus: IAsyncEventBus,
) -> None:
    uow = StubUnitOfWork()
    service, _ = _build_service(uow, async_event_bus)
    _, platform, _, _, event = _seed_event_context(uow)
    other_platform = _seed_platform(uow, app_id=1, platform="android")

    expected = uow.postback_rule_repo.save(
        build_postback_rule_entity(
            platform_app_id=platform.platform_id or 0,
            trigger_type="conversion",
            event_key="purchase",
        )
    )
    uow.postback_rule_repo.save(
        build_postback_rule_entity(
            platform_app_id=platform.platform_id or 0,
            trigger_type="metric",
            event_key="purchase",
        )
    )
    uow.postback_rule_repo.save(
        build_postback_rule_entity(
            platform_app_id=platform.platform_id or 0,
            trigger_type="conversion",
            event_key="signup",
        )
    )
    uow.postback_rule_repo.save(
        build_postback_rule_entity(
            platform_app_id=other_platform.platform_id or 0,
            trigger_type="conversion",
            event_key="purchase",
        )
    )

    rules = service.evaluate(
        build_admin_evaluate_postback_rule_command(
            event_id=event.event_id,
            trigger_type="conversion",
            event_key="purchase",
        )
    )

    assert rules == [expected]
    assert uow.commit_count == 1
    assert uow.rollback_count == 0


def test_build_params_resolves_current_snapshot_and_fallback_fields() -> None:
    uow = StubUnitOfWork()
    app, platform, click, install, event = _seed_event_context(uow)
    uow.current_param_repo.save(
        build_current_param_entity(
            click_id=click.click_id,
            param_key="utm_source",
            value_string="organic",
        )
    )
    template = PostbackTemplateEntity.from_dict(
        {
            "current_value": "{current.utm_source}",
            "snapshot_value": "{snapshot.campaign}",
            "click_id": "{click_id}",
            "user_id": "{user_id}",
            "app_code": "{app_code}",
            "platform": "{platform}",
            "timestamp": "{timestamp}",
            "amount_usd": "{amount_usd}",
            "raw_amount": "{raw_amount}",
            "geo": "{geo}",
            "ip": "{ip}",
            "ua": "{ua}",
        }
    )

    params = PostbackService.build_params(uow, template, event.event_id)

    assert params == {
        "current_value": "organic",
        "snapshot_value": "spring",
        "click_id": click.click_id,
        "user_id": install.app_user_id,
        "app_code": app.code_slug,
        "platform": platform.platform,
        "timestamp": event.event_time_utc,
        "amount_usd": event.amount_usd,
        "raw_amount": event.amount,
        "geo": "US",
        "ip": "203.0.113.10",
        "ua": "PartnerBot/1.0",
    }


@pytest.mark.parametrize(
    ("data_type", "current_value_kwargs", "expected"),
    CURRENT_PARAM_TYPE_CASES,
)
def test_build_params_resolves_current_values_by_param_definition_type(
    data_type: str,
    current_value_kwargs: dict[str, object],
    expected: object,
) -> None:
    uow = StubUnitOfWork()
    _, platform, click, _, event = _seed_event_context(uow)
    _seed_typed_current_param(
        uow,
        app_id=platform.app_id,
        click_id=click.click_id,
        machine_key="typed_value",
        data_type=data_type,
        current_value_kwargs=current_value_kwargs,
    )
    template = PostbackTemplateEntity.from_dict({"typed_value": "{current.typed_value}"})

    params = PostbackService.build_params(uow, template, event.event_id)

    assert params == {"typed_value": expected}


def test_build_params_returns_none_for_missing_related_data() -> None:
    uow = StubUnitOfWork()
    platform = _seed_platform(uow, app_id=1, platform="ios")
    click = uow.click_repo.insert(
        build_click_entity(
            click_id="click-1",
            app_platform_id=platform.platform_id or 0,
        )
    )
    event = uow.event_repo.insert(
        build_event_entity(
            event_id="evt-1",
            click_id=click.click_id,
            payload={},
            amount=None,
            amount_usd=None,
        )
    )
    template = PostbackTemplateEntity.from_dict(
        {
            "current_value": "{current.utm_source}",
            "snapshot_value": "{snapshot.campaign}",
            "user_id": "{user_id}",
            "app_code": "{app_code}",
            "geo": "{geo}",
            "ip": "{ip}",
            "ua": "{ua}",
        }
    )

    params = PostbackService.build_params(uow, template, event.event_id)

    assert params == {
        "current_value": None,
        "snapshot_value": None,
        "user_id": None,
        "app_code": None,
        "geo": None,
        "ip": None,
        "ua": None,
    }


def test_build_params_returns_none_when_platform_context_is_missing() -> None:
    uow = StubUnitOfWork()
    click = uow.click_repo.insert(
        build_click_entity(
            click_id="click-1",
            app_platform_id=999,
        )
    )
    event = uow.event_repo.insert(
        build_event_entity(
            event_id="evt-1",
            click_id=click.click_id,
            payload={"geo": "US"},
        )
    )
    template = PostbackTemplateEntity.from_dict(
        {
            "platform": "{platform}",
            "app_code": "{app_code}",
            "geo": "{geo}",
        }
    )

    params = PostbackService.build_params(uow, template, event.event_id)

    assert params == {
        "platform": None,
        "app_code": None,
        "geo": None,
    }


def test_build_params_returns_none_when_event_is_missing() -> None:
    uow = StubUnitOfWork()
    template = PostbackTemplateEntity.from_dict(
        {
            "current_value": "{current.utm_source}",
            "snapshot_value": "{snapshot.campaign}",
            "click_id": "{click_id}",
        }
    )

    params = PostbackService.build_params(uow, template, "missing-event")

    assert params == {
        "current_value": None,
        "snapshot_value": None,
        "click_id": None,
    }


def test_build_auth_params_resolves_latest_active_platform_secrets() -> None:
    uow = StubUnitOfWork()
    _, platform, _, _, _ = _seed_event_context(uow)
    _seed_secret(
        uow,
        platform_id=platform.platform_id or 0,
        code="api_key",
        encrypted_value="enc::old",
        version=1.0,
    )
    _seed_secret(
        uow,
        platform_id=platform.platform_id or 0,
        code="api_key",
        encrypted_value="enc::new",
        version=2.0,
    )

    auth = PostbackService.build_auth_params(
        uow,
        {"Authorization": "api_key"},
        platform_id=platform.platform_id or 0,
    )

    assert auth == {"Authorization": "enc::new"}


def test_build_auth_params_uses_requested_platform_context() -> None:
    uow = StubUnitOfWork()
    uow.app_repo.save(build_app_entity(app_id=1, code_slug="test-app"))
    ios = _seed_platform(uow, app_id=1, platform="ios")
    android = _seed_platform(uow, app_id=1, platform="android")
    _seed_secret(
        uow,
        platform_id=ios.platform_id or 0,
        code="api_key",
        encrypted_value="enc::ios-secret",
        version=1.0,
    )
    _seed_secret(
        uow,
        platform_id=android.platform_id or 0,
        code="api_key",
        encrypted_value="enc::android-secret",
        version=99.0,
    )

    auth = PostbackService.build_auth_params(
        uow,
        {"Authorization": "api_key"},
        platform_id=ios.platform_id or 0,
    )

    assert auth == {"Authorization": "enc::ios-secret"}


def test_build_auth_params_raises_for_unknown_secret_template() -> None:
    uow = StubUnitOfWork()
    _, platform, _, _, _ = _seed_event_context(uow)

    with pytest.raises(GeneralException):
        PostbackService.build_auth_params(
            uow,
            {"Authorization": "missing-secret"},
            platform_id=platform.platform_id or 0,
        )


def test_build_auth_params_raises_when_active_secret_is_missing() -> None:
    uow = StubUnitOfWork()
    _, platform, _, _, _ = _seed_event_context(uow)
    uow.secret_template_repo.save(build_secret_template_entity(code="api_key"))

    with pytest.raises(GeneralException):
        PostbackService.build_auth_params(
            uow,
            {"Authorization": "api_key"},
            platform_id=platform.platform_id or 0,
        )


def test_execute_raises_when_rule_does_not_exist(
    async_event_bus: IAsyncEventBus,
) -> None:
    async def scenario() -> None:
        uow = StubUnitOfWork()
        service, requester = _build_service(uow, async_event_bus)

        with pytest.raises(GeneralException):
            await service.execute(build_admin_execute_postback_rule_command(postback_rule_id=999))

        assert requester.calls == []
        assert uow.commit_count == 0
        assert uow.rollback_count == 1

    asyncio.run(scenario())


@pytest.mark.parametrize(
    ("data_type", "current_value_kwargs", "expected"),
    CURRENT_PARAM_TYPE_CASES,
)
def test_execute_builds_request_and_calls_requester(
    async_event_bus: IAsyncEventBus,
    data_type: str,
    current_value_kwargs: dict[str, object],
    expected: object,
) -> None:
    async def scenario() -> None:
        uow = StubUnitOfWork()
        service, requester = _build_service(uow, async_event_bus)
        _, platform, click, _, event = _seed_event_context(uow)
        _seed_typed_current_param(
            uow,
            app_id=platform.app_id,
            click_id=click.click_id,
            machine_key="typed_value",
            data_type=data_type,
            current_value_kwargs=current_value_kwargs,
        )
        _seed_secret(
            uow,
            platform_id=platform.platform_id or 0,
            code="api_key",
            encrypted_value="enc::api-key-v2",
            version=2.0,
        )
        rule = uow.postback_rule_repo.save(
            build_postback_rule_entity(
                platform_app_id=platform.platform_id or 0,
                endpoint_url="https://example.com/postback/conversion",
                trigger_type="conversion",
                http_method="POST",
                headers={"X-Test": "postback"},
                auth_params={"Authorization": "api_key"},
                template=PostbackTemplateEntity.from_dict(
                    {
                        "click_id": "{click_id}",
                        "campaign": "{current.typed_value}",
                        "geo": "{geo}",
                    }
                ),
            )
        )

        await service.execute(
            build_admin_execute_postback_rule_command(
                postback_rule_id=rule.rule_id or 0,
                event_id=event.event_id,
            )
        )

        assert len(requester.calls) == 1
        call = requester.calls[0]
        assert call.method == "postback"
        assert call.args[0] == "https://example.com/postback/conversion"
        assert call.args[1] == "POST"
        assert call.args[2] == {"X-Test": "postback"}
        assert call.args[3] == {"Authorization": "enc::api-key-v2"}
        assert call.args[4] == {
            "click_id": click.click_id,
            "campaign": expected,
            "geo": "US",
        }
        assert requester.final_urls == [
            _build_expected_final_url(
                "https://example.com/postback/conversion",
                {
                    "click_id": click.click_id,
                    "campaign": expected,
                    "geo": "US",
                },
                http_method="POST",
            )
        ]
        assert uow.commit_count == 1
        assert uow.rollback_count == 0

    asyncio.run(scenario())


@pytest.mark.parametrize(
    ("data_type", "current_value_kwargs", "expected"),
    CURRENT_PARAM_TYPE_CASES,
)
def test_execute_builds_get_request_and_calls_requester(
    async_event_bus: IAsyncEventBus,
    data_type: str,
    current_value_kwargs: dict[str, object],
    expected: object,
) -> None:
    async def scenario() -> None:
        uow = StubUnitOfWork()
        service, requester = _build_service(uow, async_event_bus)
        _, platform, click, _, event = _seed_event_context(uow)
        _seed_typed_current_param(
            uow,
            app_id=platform.app_id,
            click_id=click.click_id,
            machine_key="typed_value",
            data_type=data_type,
            current_value_kwargs=current_value_kwargs,
        )
        _seed_secret(
            uow,
            platform_id=platform.platform_id or 0,
            code="api_key",
            encrypted_value="enc::api-key-v1",
        )
        rule = uow.postback_rule_repo.save(
            build_postback_rule_entity(
                platform_app_id=platform.platform_id or 0,
                endpoint_url="https://example.com/postback/install",
                trigger_type="conversion",
                http_method="GET",
                headers={"X-Mode": "query"},
                auth_params={"Authorization": "api_key"},
                template=PostbackTemplateEntity.from_dict(
                    {
                        "click_id": "{click_id}",
                        "campaign": "{current.typed_value}",
                    }
                ),
            )
        )

        await service.execute(
            build_admin_execute_postback_rule_command(
                postback_rule_id=rule.rule_id or 0,
                event_id=event.event_id,
            )
        )

        assert len(requester.calls) == 1
        call = requester.calls[0]
        assert call.method == "postback"
        assert call.args[0] == "https://example.com/postback/install"
        assert call.args[1] == "GET"
        assert call.args[2] == {"X-Mode": "query"}
        assert call.args[3] == {"Authorization": "enc::api-key-v1"}
        assert call.args[4] == {
            "click_id": click.click_id,
            "campaign": expected,
        }
        assert requester.final_urls == [
            _build_expected_final_url(
                "https://example.com/postback/install",
                {
                    "click_id": click.click_id,
                    "campaign": expected,
                },
                http_method="GET",
            )
        ]
        assert uow.commit_count == 1
        assert uow.rollback_count == 0

    asyncio.run(scenario())


def test_execute_propagates_requester_failures_and_rolls_back(
    async_event_bus: IAsyncEventBus,
) -> None:
    async def scenario() -> None:
        uow = StubUnitOfWork()
        service, requester = _build_service(uow, async_event_bus)
        _, platform, _, _, event = _seed_event_context(uow)
        _seed_secret(
            uow,
            platform_id=platform.platform_id or 0,
            code="api_key",
            encrypted_value="enc::api-key-v1",
        )
        rule = uow.postback_rule_repo.save(
            build_postback_rule_entity(
                platform_app_id=platform.platform_id or 0,
                auth_params={"Authorization": "api_key"},
                template=PostbackTemplateEntity.from_dict({"click_id": "{click_id}"}),
            )
        )
        requester.error = RuntimeError("boom")

        with pytest.raises(RuntimeError, match="boom"):
            await service.execute(
                build_admin_execute_postback_rule_command(
                    postback_rule_id=rule.rule_id or 0,
                    event_id=event.event_id,
                )
            )

        assert len(requester.calls) == 1
        assert uow.commit_count == 0
        assert uow.rollback_count == 1

    asyncio.run(scenario())
