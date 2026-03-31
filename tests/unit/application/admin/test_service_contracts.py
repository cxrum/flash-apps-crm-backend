from __future__ import annotations

from typing import get_type_hints

from app.application.admin.definitions.commands import CreateConversionDefinitionCommand, CreateParamDefinitionCommand, ListConversionDefinitionsCommand, ListMetricDefinitionsCommand, ListParamDefinitionsCommand, UpdateConversionDefinitionCommand, UpdateMetricDefinitionCommand, UpdateParamDefinitionCommand
from app.application.admin.definitions.responses import CreateConversionDefinitionResponse, CreateMetricDefinitionResponse, CreateParamDefinitionResponse, ListConversionDefinitionsResponse, ListMetricDefinitionsResponse, ListParamDefinitionsResponse, UpdateConversionDefinitionResponse, UpdateMetricDefinitionResponse, UpdateParamDefinitionResponse
from app.application.admin.definitions.service import DefinitionsService
from app.application.admin.logs.commands import (
    ListAuditLogCommand,
)
from app.application.admin.logs.commands import ListClickLogsCommand, ListEventLogsCommand
from app.application.admin.logs.responses import ListAuditLogsResponse, ListClickLogsResponse, ListRawEventsResponse
from app.application.admin.logs.service import LogsService
from app.application.admin.secrets.commands import CreateAppSecretCommand, CreateSecretTemplateCommand, ListAppSecretsCommand, ListSecretTemplatesCommand, UpdateAppSecretCommand
from app.application.admin.secrets.responses import (
    ListSecretTemplatesResponse,
)
from app.application.admin.secrets.responses import CreateAppSecretResponse, CreateSecretTemplateResponse, ListAppSecretsResponse, UpdateAppSecretResponse
from app.application.admin.secrets.service import SecretsService
from app.application.admin.definitions.commands import CreateMetricDefinitionCommand


def test_defenitions_service_method_contracts_use_command_and_response_types() -> None:
    assert get_type_hints(DefinitionsService.list_metrics) == {
        "command": ListMetricDefinitionsCommand,
        "return": ListMetricDefinitionsResponse,
    }
    assert get_type_hints(DefinitionsService.create_metric_definition) == {
        "command": CreateMetricDefinitionCommand,
        "return": CreateMetricDefinitionResponse,
    }
    assert get_type_hints(DefinitionsService.update_metric_definition) == {
        "command": UpdateMetricDefinitionCommand,
        "return": UpdateMetricDefinitionResponse,
    }
    assert get_type_hints(DefinitionsService.list_conversions) == {
        "command": ListConversionDefinitionsCommand,
        "return": ListConversionDefinitionsResponse,
    }
    assert get_type_hints(DefinitionsService.create_conversion_definition) == {
        "command": CreateConversionDefinitionCommand,
        "return": CreateConversionDefinitionResponse,
    }
    assert get_type_hints(DefinitionsService.update_conversion_definition) == {
        "command": UpdateConversionDefinitionCommand,
        "return": UpdateConversionDefinitionResponse,
    }
    assert get_type_hints(DefinitionsService.list_params) == {
        "command": ListParamDefinitionsCommand,
        "return": ListParamDefinitionsResponse,
    }
    assert get_type_hints(DefinitionsService.create_param_definition) == {
        "command": CreateParamDefinitionCommand,
        "return": CreateParamDefinitionResponse,
    }
    assert get_type_hints(DefinitionsService.update_param_definition) == {
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
        "command": ListAuditLogCommand,
        "return": ListAuditLogsResponse,
    }
