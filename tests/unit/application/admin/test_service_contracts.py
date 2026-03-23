from __future__ import annotations

from typing import get_type_hints

from app.application.admin.defenitions.service import DefenitionsService
from app.application.admin.entities import (
    CreateAppSecretCommand,
    CreateConversionDefinitionCommand,
    CreateMetricDefinitionCommand,
    CreateParamDefinitionCommand,
    CreateSecretTemplateCommand,
    GetAuditLogCommand,
    ListClickLogsCommand,
    ListConversionDefinitionsCommand,
    ListEventLogsCommand,
    ListMetricDefinitionsCommand,
    ListParamDefinitionsCommand,
    ListAppSecretsCommand,
    ListSecretTemplatesCommand,
    UpdateAppSecretCommand,
    UpdateConversionDefinitionCommand,
    UpdateMetricDefinitionCommand,
    UpdateParamDefinitionCommand,
)
from app.application.admin.logs.service import LogsService
from app.application.admin.responses import (
    CreateAppSecretResponse,
    CreateConversionDefinitionResponse,
    CreateMetricDefinitionResponse,
    CreateParamDefinitionResponse,
    CreateSecretTemplateResponse,
    ListAppSecretsResponse,
    ListAuditLogsResponse,
    ListClickLogsResponse,
    ListConversionDefinitionsResponse,
    ListMetricDefinitionsResponse,
    ListParamDefinitionsResponse,
    ListRawEventsResponse,
    ListSecretTemplatesResponse,
    UpdateAppSecretResponse,
    UpdateConversionDefinitionResponse,
    UpdateMetricDefinitionResponse,
    UpdateParamDefinitionResponse,
)
from app.application.admin.secrets.service import SecretsService


def test_defenitions_service_method_contracts_use_command_and_response_types() -> None:
    assert get_type_hints(DefenitionsService.list_metrics) == {
        "command": ListMetricDefinitionsCommand,
        "return": ListMetricDefinitionsResponse,
    }
    assert get_type_hints(DefenitionsService.create_metric_defenition) == {
        "command": CreateMetricDefinitionCommand,
        "return": CreateMetricDefinitionResponse,
    }
    assert get_type_hints(DefenitionsService.update_metric_defenition) == {
        "command": UpdateMetricDefinitionCommand,
        "return": UpdateMetricDefinitionResponse,
    }
    assert get_type_hints(DefenitionsService.list_conversions) == {
        "command": ListConversionDefinitionsCommand,
        "return": ListConversionDefinitionsResponse,
    }
    assert get_type_hints(DefenitionsService.create_conversion_defenition) == {
        "command": CreateConversionDefinitionCommand,
        "return": CreateConversionDefinitionResponse,
    }
    assert get_type_hints(DefenitionsService.update_conversion_defenition) == {
        "command": UpdateConversionDefinitionCommand,
        "return": UpdateConversionDefinitionResponse,
    }
    assert get_type_hints(DefenitionsService.list_params) == {
        "command": ListParamDefinitionsCommand,
        "return": ListParamDefinitionsResponse,
    }
    assert get_type_hints(DefenitionsService.create_param_defenition) == {
        "command": CreateParamDefinitionCommand,
        "return": CreateParamDefinitionResponse,
    }
    assert get_type_hints(DefenitionsService.update_param_defenition) == {
        "command": UpdateParamDefinitionCommand,
        "return": UpdateParamDefinitionResponse,
    }


def test_secrets_service_method_contracts_use_command_and_response_types() -> None:
    assert get_type_hints(SecretsService.list_secret_templates) == {
        "command": ListSecretTemplatesCommand,
        "return": ListSecretTemplatesResponse,
    }
    assert get_type_hints(SecretsService.create_secret_template) == {
        "command": CreateSecretTemplateCommand,
        "return": CreateSecretTemplateResponse,
    }
    assert get_type_hints(SecretsService.create_app_secret) == {
        "command": CreateAppSecretCommand,
        "return": CreateAppSecretResponse,
    }
    assert get_type_hints(SecretsService.list_app_secrets) == {
        "command": ListAppSecretsCommand,
        "return": ListAppSecretsResponse,
    }
    assert get_type_hints(SecretsService.update_app_secret) == {
        "command": UpdateAppSecretCommand,
        "return": UpdateAppSecretResponse,
    }


def test_logs_service_method_contracts_use_command_and_response_types() -> None:
    assert get_type_hints(LogsService.list_clicks) == {
        "command": ListClickLogsCommand,
        "return": ListClickLogsResponse,
    }
    assert get_type_hints(LogsService.list_raw_events) == {
        "command": ListEventLogsCommand,
        "return": ListRawEventsResponse,
    }
    assert get_type_hints(LogsService.list_audit_logs) == {
        "command": GetAuditLogCommand,
        "return": ListAuditLogsResponse,
    }
