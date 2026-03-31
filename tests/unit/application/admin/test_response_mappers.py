from __future__ import annotations

from typing import get_type_hints

from app.application.admin.definitions.responses import ConversionDefinitionResponseEntry, CreateConversionDefinitionResponse, CreateMetricDefinitionResponse, CreateParamDefinitionResponse, ListConversionDefinitionsResponse, ListMetricDefinitionsResponse, ListParamDefinitionsResponse, MetricDefinitionResponseEntry, ParamDefinitionResponseEntry
from app.application.admin.logs.responses import AuditLogResponseEntry, ClickLogResponseEntry, ListAuditLogsResponse, ListClickLogsResponse, ListRawEventsResponse, RawEventLogResponseEntry
from app.application.admin.mappers import AdminResponseMapper
from app.application.admin.responses import (
    AppSecretResponseEntry,
)
from app.application.admin.secrets.responses import CreateAppSecretResponse, CreateSecretTemplateResponse, ListAppSecretsResponse, ListSecretTemplatesResponse, SecretTemplateResponseEntry, UpdateAppSecretResponse
from tests.unit.builders.entities import (
    build_app_secret_entity,
    build_audit_log_entity,
    build_click_entity,
    build_conversion_definition_entity,
    build_event_entity,
    build_metric_definition_entity,
    build_param_definition_entity,
    build_secret_template_entity,
)


def test_admin_response_mapper_converts_definition_entities_to_response_entries() -> None:
    metric = build_metric_definition_entity(metric_definition_id=10)
    conversion = build_conversion_definition_entity(conversion_definition_id=11)
    param = build_param_definition_entity(param_definition_id=12)
    secret_template = build_secret_template_entity(template_id=13)
    app_secret = build_app_secret_entity(secret_id=14)

    metric_response = AdminResponseMapper.create_metric_definition_from_domain(metric)
    conversion_response = AdminResponseMapper.create_conversion_definition_from_domain(conversion)
    param_response = AdminResponseMapper.create_param_definition_from_domain(param)
    secret_response = AdminResponseMapper.create_secret_template_from_domain(secret_template)
    app_secret_response = AdminResponseMapper.create_app_secret_from_domain(app_secret)

    assert isinstance(metric_response.metric_definition, MetricDefinitionResponseEntry)
    assert metric_response.metric_definition.metric_definition_id == 10
    assert isinstance(conversion_response.conversion_definition, ConversionDefinitionResponseEntry)
    assert conversion_response.conversion_definition.conversion_definition_id == 11
    assert isinstance(param_response.param_definition, ParamDefinitionResponseEntry)
    assert param_response.param_definition.param_definition_id == 12
    assert isinstance(secret_response.secret_template, SecretTemplateResponseEntry)
    assert secret_response.secret_template.template_id == 13
    assert isinstance(app_secret_response.app_secret, AppSecretResponseEntry)
    assert app_secret_response.app_secret.secret_id == 14


def test_admin_response_wrappers_reference_application_response_entries() -> None:
    assert get_type_hints(ListMetricDefinitionsResponse) == {
        "metric_definitions": list[MetricDefinitionResponseEntry],
    }
    assert get_type_hints(CreateMetricDefinitionResponse) == {
        "metric_definition": MetricDefinitionResponseEntry,
    }
    assert get_type_hints(ListConversionDefinitionsResponse) == {
        "conversion_definitions": list[ConversionDefinitionResponseEntry],
    }
    assert get_type_hints(CreateConversionDefinitionResponse) == {
        "conversion_definition": ConversionDefinitionResponseEntry,
    }
    assert get_type_hints(ListParamDefinitionsResponse) == {
        "param_definitions": list[ParamDefinitionResponseEntry],
    }
    assert get_type_hints(CreateParamDefinitionResponse) == {
        "param_definition": ParamDefinitionResponseEntry,
    }
    assert get_type_hints(ListSecretTemplatesResponse) == {
        "secret_templates": list[SecretTemplateResponseEntry],
    }
    assert get_type_hints(CreateSecretTemplateResponse) == {
        "secret_template": SecretTemplateResponseEntry,
    }
    assert get_type_hints(ListAppSecretsResponse) == {
        "app_secrets": list[AppSecretResponseEntry],
    }
    assert get_type_hints(CreateAppSecretResponse) == {
        "app_secret": AppSecretResponseEntry,
    }
    assert get_type_hints(UpdateAppSecretResponse) == {
        "app_secret": AppSecretResponseEntry,
    }
    assert get_type_hints(ListClickLogsResponse) == {
        "clicks": list[ClickLogResponseEntry],
    }
    assert get_type_hints(ListRawEventsResponse) == {
        "events": list[RawEventLogResponseEntry],
    }
    assert get_type_hints(ListAuditLogsResponse) == {
        "audit_logs": list[AuditLogResponseEntry],
    }


def test_admin_response_mapper_copies_mutable_log_payloads_into_response_entries() -> None:
    click = build_click_entity(
        raw_query={"utm_source": "ads"},
        geo={"country": "US"},
        normalized_params={"utm_source": "ads"},
    )
    event = build_event_entity(payload={"source": "sdk"})
    audit_log = build_audit_log_entity(
        old_value={"status": "draft"},
        new_value=[{"status": "active"}],
    )

    click_entry = AdminResponseMapper.click_log_from_domain(click)
    event_entry = AdminResponseMapper.raw_event_from_domain(event)
    audit_entry = AdminResponseMapper.audit_log_from_domain(audit_log)

    assert isinstance(click_entry, ClickLogResponseEntry)
    assert isinstance(event_entry, RawEventLogResponseEntry)
    assert isinstance(audit_entry, AuditLogResponseEntry)

    click.raw_query["utm_source"] = "organic"
    event.payload["source"] = "api"
    audit_log.new_value.append({"status": "paused"})

    assert click_entry.raw_query == {"utm_source": "ads"}
    assert event_entry.payload == {"source": "sdk"}
    assert audit_entry.new_value == [{"status": "active"}]
