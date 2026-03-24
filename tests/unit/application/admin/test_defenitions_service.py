from __future__ import annotations

from dataclasses import dataclass

import pytest

from app.application.admin.defenitions.service import DefenitionsService
from app.application.exceptions import ApplicationError
from tests.unit.builders.commands import (
    build_admin_create_conversion_definition_command,
    build_admin_create_metric_definition_command,
    build_admin_create_param_definition_command,
    build_admin_list_conversion_definitions_command,
    build_admin_list_metric_definitions_command,
    build_admin_list_param_definitions_command,
    build_admin_update_conversion_definition_command,
    build_admin_update_metric_definition_command,
    build_admin_update_param_definition_command,
)
from tests.unit.builders.entities import (
    build_app_entity,
    build_conversion_definition_entity,
    build_metric_definition_entity,
    build_param_definition_entity,
)
from tests.unit.doubles.domain.uow import StubUnitOfWork, StubUoWFactory


@dataclass(frozen=True)
class ChechUserAccessToAppCommand:
    app_id: int
    crm_user_id: int


class StubCrmUsersService:
    def __init__(self, *, has_access: bool = True) -> None:
        self.has_access = has_access
        self.calls: list[ChechUserAccessToAppCommand] = []

    def check_user_app_access(self, app_id: int, crm_user_id: int | None) -> None:
        if crm_user_id is None:
            raise ApplicationError("CRM user context is required")

        has_access = self.user_has_acces_to_app(
            ChechUserAccessToAppCommand(
                app_id=app_id,
                crm_user_id=crm_user_id,
            )
        )
        if not has_access:
            raise ApplicationError(f"User {crm_user_id} does not have access to app {app_id}")

    def user_has_acces_to_app(self, command: ChechUserAccessToAppCommand) -> bool:
        self.calls.append(command)
        return self.has_access

    def is_user_admin_permision_access(self, crm_user_id: int | None, app_id: int) -> bool:
        return True
    
    def is_user_manager_permision_access(self, crm_user_id: int | None, app_id: int) -> bool:
        return True
        

def test_list_metrics_returns_response_entries_for_app() -> None:
    uow = StubUnitOfWork()
    uow.metric_definition_repo.save(build_metric_definition_entity(app_id=1, metric_definition_id=1))
    uow.metric_definition_repo.save(build_metric_definition_entity(app_id=1, metric_definition_id=2))
    uow.metric_definition_repo.save(build_metric_definition_entity(app_id=2, metric_definition_id=3))
    user_service = StubCrmUsersService()
    service = DefenitionsService(StubUoWFactory(uow), user_service)

    response = service.list_metrics(
        build_admin_list_metric_definitions_command(app_id=1, crm_user_id=77)
    )

    assert [item.metric_definition_id for item in response.metric_definitions] == [1, 2]
    assert user_service.calls == [ChechUserAccessToAppCommand(app_id=1, crm_user_id=77)]


def test_create_metric_definition_saves_and_maps_metric() -> None:
    uow = StubUnitOfWork()
    uow.app_repo.save(build_app_entity(app_id=1))
    service = DefenitionsService(StubUoWFactory(uow), StubCrmUsersService())

    response = service.create_metric_defenition(
        build_admin_create_metric_definition_command(
            app_id=1,
            crm_user_id=77,
            key="session_start",
            name="Session Start",
            description="Tracks session starts",
            is_active=False,
        )
    )

    saved = uow.metric_definition_repo.get_by_id(response.metric_definition.metric_definition_id or 0)
    assert saved is not None
    assert saved.machine_key == "session_start"
    assert saved.display_name == "Session Start"
    assert saved.enabled is False


def test_update_metric_definition_updates_existing_metric() -> None:
    uow = StubUnitOfWork()
    existing = uow.metric_definition_repo.save(
        build_metric_definition_entity(
            app_id=1,
            metric_definition_id=1,
            machine_key="first_open",
            display_name="First Open",
            description="Old metric",
            enabled=True,
        )
    )
    service = DefenitionsService(StubUoWFactory(uow), StubCrmUsersService())

    response = service.update_metric_defenition(
        build_admin_update_metric_definition_command(
            app_id=1,
            crm_user_id=77,
            metric_definition_id=existing.metric_definition_id,
            name="Session Start",
            is_active=False,
        )
    )

    saved = uow.metric_definition_repo.get_by_id(response.metric_definition.metric_definition_id or 0)
    assert saved is not None
    assert saved.metric_definition_id == existing.metric_definition_id
    assert saved.machine_key == "first_open_updated"
    assert saved.display_name == "Session Start"
    assert saved.enabled is False


def test_list_conversions_returns_response_entries_for_app() -> None:
    uow = StubUnitOfWork()
    uow.conversion_definition_repo.save(build_conversion_definition_entity(app_id=1, conversion_definition_id=1))
    uow.conversion_definition_repo.save(build_conversion_definition_entity(app_id=2, conversion_definition_id=2))
    user_service = StubCrmUsersService()
    service = DefenitionsService(StubUoWFactory(uow), user_service)

    response = service.list_conversions(
        build_admin_list_conversion_definitions_command(app_id=1, crm_user_id=88)
    )

    assert [item.conversion_definition_id for item in response.conversion_definitions] == [1]
    assert user_service.calls == [ChechUserAccessToAppCommand(app_id=1, crm_user_id=88)]


def test_create_conversion_definition_saves_explicit_revenue_flags() -> None:
    uow = StubUnitOfWork()
    uow.app_repo.save(build_app_entity(app_id=1))
    service = DefenitionsService(StubUoWFactory(uow), StubCrmUsersService())

    response = service.create_conversion_defenition(
        build_admin_create_conversion_definition_command(
            app_id=1,
            crm_user_id=77,
            key="purchase",
            name="Purchase",
            revenue_enabled=True,
            expects_amount=True,
            expects_currency=True,
        )
    )

    saved = uow.conversion_definition_repo.get_by_id(
        response.conversion_definition.conversion_definition_id or 0
    )
    assert saved is not None
    assert saved.machine_key == "purchase"
    assert saved.revenue_enabled is True
    assert saved.expects_amount is True
    assert saved.expects_currency is True


def test_update_conversion_definition_updates_existing_conversion() -> None:
    uow = StubUnitOfWork()
    existing = uow.conversion_definition_repo.save(
        build_conversion_definition_entity(
            app_id=1,
            conversion_definition_id=1,
            machine_key="purchase",
            display_name="Purchase",
            revenue_enabled=True,
            expects_amount=True,
            expects_currency=True,
            dedup_mode="none",
        )
    )
    service = DefenitionsService(StubUoWFactory(uow), StubCrmUsersService())

    response = service.update_conversion_defenition(
        build_admin_update_conversion_definition_command(
            app_id=1,
            crm_user_id=77,
            conversion_definition_id=existing.conversion_definition_id,
            revenue_enabled=False,
            expects_amount=False,
            expects_currency=False,
            dedup_mode="click",
        )
    )

    saved = uow.conversion_definition_repo.get_by_id(
        response.conversion_definition.conversion_definition_id or 0
    )
    assert saved is not None
    assert saved.conversion_definition_id == existing.conversion_definition_id
    assert saved.machine_key == "purchase_updated"
    assert saved.revenue_enabled is False
    assert saved.expects_amount is False
    assert saved.expects_currency is False
    assert saved.dedup_mode == "click"


def test_list_params_returns_response_entries_for_app() -> None:
    uow = StubUnitOfWork()
    uow.param_definition_repo.save(build_param_definition_entity(app_id=1, param_definition_id=1))
    uow.param_definition_repo.save(build_param_definition_entity(app_id=1, param_definition_id=2))
    uow.param_definition_repo.save(build_param_definition_entity(app_id=3, param_definition_id=3))
    user_service = StubCrmUsersService()
    service = DefenitionsService(StubUoWFactory(uow), user_service)

    response = service.list_params(
        build_admin_list_param_definitions_command(app_id=1, crm_user_id=91)
    )

    assert [item.param_definition_id for item in response.param_definitions] == [1, 2]
    assert user_service.calls == [ChechUserAccessToAppCommand(app_id=1, crm_user_id=91)]


def test_create_param_definition_saves_param() -> None:
    uow = StubUnitOfWork()
    uow.app_repo.save(build_app_entity(app_id=1))
    service = DefenitionsService(StubUoWFactory(uow), StubCrmUsersService())

    response = service.create_param_defenition(
        build_admin_create_param_definition_command(
            app_id=1,
            crm_user_id=77,
            key="utm_campaign",
            label="UTM Campaign",
            param_type="string",
        )
    )

    saved = uow.param_definition_repo.get_by_id(response.param_definition.param_definition_id or 0)
    assert saved is not None
    assert saved.machine_key == "utm_campaign"
    assert saved.display_name == "UTM Campaign"
    assert saved.data_type == "string"
    assert saved.filterable is False


def test_update_param_definition_updates_existing_param() -> None:
    uow = StubUnitOfWork()
    existing = uow.param_definition_repo.save(
        build_param_definition_entity(
            app_id=1,
            param_definition_id=1,
            display_name="UTM Source",
            machine_key="utm_source",
            data_type="string",
            visible_in_stats=False,
            groupable=False,
        )
    )
    service = DefenitionsService(StubUoWFactory(uow), StubCrmUsersService())

    response = service.update_param_defenition(
        build_admin_update_param_definition_command(
            app_id=1,
            crm_user_id=77,
            param_definition_id=existing.param_definition_id,
            label="Traffic Source",
            visible_in_stats=True,
            groupable=True,
        )
    )

    saved = uow.param_definition_repo.get_by_id(response.param_definition.param_definition_id or 0)
    assert saved is not None
    assert saved.param_definition_id == existing.param_definition_id
    assert saved.machine_key == "utm_source_updated"
    assert saved.display_name == "Traffic Source"
    assert saved.visible_in_stats is True
    assert saved.groupable is True


def test_definition_service_rejects_missing_user_context() -> None:
    service = DefenitionsService(StubUoWFactory(StubUnitOfWork()), StubCrmUsersService())

    with pytest.raises(Exception):
        service.list_metrics(build_admin_list_metric_definitions_command(app_id=1, crm_user_id=None))


def test_definition_service_rejects_user_without_access() -> None:
    service = DefenitionsService(
        StubUoWFactory(StubUnitOfWork()),
        StubCrmUsersService(has_access=False),
    )

    with pytest.raises(ApplicationError, match="does not have access"):
        service.list_conversions(
            build_admin_list_conversion_definitions_command(app_id=1, crm_user_id=77)
        )


def test_create_definition_methods_reject_unknown_app() -> None:
    service = DefenitionsService(StubUoWFactory(StubUnitOfWork()), StubCrmUsersService(has_access=False))

    with pytest.raises(ApplicationError):
        service.create_metric_defenition(
            build_admin_create_metric_definition_command(
                app_id=999,
                crm_user_id=77,
                key="first_open",
                name="First Open",
            )
        )


@pytest.mark.parametrize(
    ("method_name", "command_builder", "expected_message"),
    [
        ("create_metric_defenition", build_admin_create_metric_definition_command, "Metric key is required"),
        (
            "create_conversion_defenition",
            build_admin_create_conversion_definition_command,
            "Conversion key is required",
        ),
        ("create_param_defenition", build_admin_create_param_definition_command, "Param key is required"),
    ],
)
def test_create_definition_methods_validate_required_keys(
    method_name: str,
    command_builder,
    expected_message: str,
) -> None:
    service = DefenitionsService(StubUoWFactory(StubUnitOfWork()), StubCrmUsersService())

    with pytest.raises(ApplicationError, match=expected_message):
        getattr(service, method_name)(command_builder(app_id=1, crm_user_id=77, key=" "))
