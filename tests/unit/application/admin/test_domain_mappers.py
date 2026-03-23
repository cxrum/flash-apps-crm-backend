from __future__ import annotations

import pytest

from app.application.admin.entities import (
    CreateConversionDefinitionCommand,
    CreateMetricDefinitionCommand,
    CreateParamDefinitionCommand,
    CreateSecretTemplateCommand,
    UpdateConversionDefinitionCommand,
    UpdateMetricDefinitionCommand,
    UpdateParamDefinitionCommand,
)
from app.application.admin.mappers import AdminDomainMapper
from tests.unit.builders.entities import (
    build_conversion_definition_entity,
    build_metric_definition_entity,
    build_param_definition_entity,
)


def test_admin_domain_mapper_maps_metric_definition_command() -> None:
    entity = AdminDomainMapper.metric_definition_from_command(
        CreateMetricDefinitionCommand(
            crm_user_id=1,
            app_id=1,
            key="first_open",
            name="First Open",
            description="Tracks first opens",
            is_active=False,
        )
    )

    assert entity.machine_key == "first_open"
    assert entity.display_name == "First Open"
    assert entity.description == "Tracks first opens"
    assert entity.enabled is False


def test_admin_domain_mapper_uses_explicit_conversion_flags_when_present() -> None:
    entity = AdminDomainMapper.conversion_definition_from_command(
        CreateConversionDefinitionCommand(
            crm_user_id=1,
            app_id=1,
            key="purchase",
            name="Purchase",
            currency="USD",
            revenue_enabled=False,
            expects_amount=False,
            expects_currency=False,
            dedup_mode="click",
        )
    )

    assert entity.machine_key == "purchase"
    assert entity.revenue_enabled is False
    assert entity.expects_amount is False
    assert entity.expects_currency is False
    assert entity.dedup_mode == "click"


def test_admin_domain_mapper_maps_param_definition_command() -> None:
    entity = AdminDomainMapper.param_definition_from_command(
        CreateParamDefinitionCommand(
            crm_user_id=1,
            app_id=1,
            key="utm_source",
            label="UTM Source",
            param_type="string",
            description="Normalized traffic source",
            visible_in_stats=True,
            groupable=True,
        )
    )

    assert entity.machine_key == "utm_source"
    assert entity.display_name == "UTM Source"
    assert entity.data_type == "string"
    assert entity.description == "Normalized traffic source"
    assert entity.visible_in_stats is True
    assert entity.groupable is True


@pytest.mark.parametrize(
    ("visibility", "expected_scope"),
    [
        ("global", "client_public"),
        ("server_private", "server_private"),
    ],
)
def test_admin_domain_mapper_maps_secret_template_command(
    visibility: str,
    expected_scope: str,
) -> None:
    entity = AdminDomainMapper.secret_template_from_command(
        CreateSecretTemplateCommand(
            crm_user_id=1,
            app_id=1,
            key="api_key",
            name="API Key",
            secret_type="text",
            visibility=visibility,
        )
    )

    assert entity.code == "api_key"
    assert entity.display_name == "API Key"
    assert entity.scope == expected_scope
    assert entity.value_type == "text"
    assert entity.is_masked is True
    assert entity.is_required is False


def test_admin_domain_mapper_updates_metric_definition_and_preserves_omitted_fields() -> None:
    existing = build_metric_definition_entity(
        metric_definition_id=7,
        machine_key="first_open",
        display_name="First Open",
        description="Old description",
        enabled=True,
    )

    entity = AdminDomainMapper.metric_definition_from_update_command(
        existing,
        UpdateMetricDefinitionCommand(
            crm_user_id=1,
            app_id=1,
            metric_definition_id=7,
            name="First Session",
        ),
    )

    assert entity.metric_definition_id == 7
    assert entity.machine_key == "first_open"
    assert entity.display_name == "First Session"
    assert entity.description == "Old description"
    assert entity.enabled is True


def test_admin_domain_mapper_updates_conversion_definition_fields() -> None:
    existing = build_conversion_definition_entity(
        conversion_definition_id=9,
        dedup_mode="none",
        revenue_enabled=True,
        expects_amount=True,
        expects_currency=True,
    )

    entity = AdminDomainMapper.conversion_definition_from_update_command(
        existing,
        UpdateConversionDefinitionCommand(
            crm_user_id=1,
            app_id=1,
            conversion_definition_id=9,
            description=None,
            revenue_enabled=False,
            dedup_mode="click",
        ),
    )

    assert entity.conversion_definition_id == 9
    assert entity.description is None
    assert entity.revenue_enabled is False
    assert entity.expects_amount is True
    assert entity.dedup_mode == "click"


def test_admin_domain_mapper_updates_param_definition_fields() -> None:
    existing = build_param_definition_entity(
        param_definition_id=11,
        display_name="UTM Source",
        machine_key="utm_source",
        data_type="string",
        description="Old description",
        visible_in_stats=False,
        groupable=False,
    )

    entity = AdminDomainMapper.param_definition_from_update_command(
        existing,
        UpdateParamDefinitionCommand(
            crm_user_id=1,
            app_id=1,
            param_definition_id=11,
            label="Traffic Source",
            description=None,
            visible_in_stats=True,
            groupable=True,
        ),
    )

    assert entity.param_definition_id == 11
    assert entity.display_name == "Traffic Source"
    assert entity.machine_key == "utm_source"
    assert entity.description is None
    assert entity.visible_in_stats is True
    assert entity.groupable is True
