from __future__ import annotations

import pytest

from app.application.admin.definitions.commands import DeleteConversionDefinitionCommand, DeleteMetricDefinitionCommand, DeleteParamDefinitionCommand, GetConversionDefinitionCommand, GetMetricDefinitionCommand, GetParamDefinitionCommand, UpdateMetricDefinitionCommand, UpdateParamDefinitionCommand
from app.application.crm_authentication.commands import (
    DeleteAppAccessCommand,
)
from app.application.admin.mappers import AdminCommandMapper
from app.application.admin.postback.commands import DeletePostbackRuleCommand, GetPostbackRuleCommand, UpdatePostbackRuleCommand
from app.application.admin.push.commands import DeletePushCampaignCommand, GetPushCampaignCommand, StartPushCampaignCommand, UpdatePushCampaignCommand
from app.application.admin.secrets.commands import DeleteAppSecretCommand, DeleteSecretTemplateCommand, GetAppSecretValueCommand, GetSecretTemplatesCommand, UpdateAppSecretCommand, UpdateSecretTemplateCommand
from app.application.crm_authentication.commands import ListUsersWithAccessCommand, ShareAppAccessCommand


@pytest.mark.parametrize(
    ("mapper_name", "payload", "expected_type", "expected_field", "expected_value"),
    [
        (
            "get_metric_from_transport",
            {"crm_user_id": 1, "app_id": 11, "metric_definition_id": 7},
            GetMetricDefinitionCommand,
            "metric_definition_id",
            7,
        ),
        (
            "update_metric_from_transport",
            {"crm_user_id": 1, "app_id": 11, "metric_definition_id": 7, "name": "Updated Metric"},
            UpdateMetricDefinitionCommand,
            "name",
            "Updated Metric",
        ),
        (
            "delete_metric_from_transport",
            {"crm_user_id": 1, "app_id": 11, "metric_definition_id": 7},
            DeleteMetricDefinitionCommand,
            "metric_definition_id",
            7,
        ),
        (
            "get_conversion_from_transport",
            {"crm_user_id": 1, "app_id": 11, "conversion_definition_id": 9},
            GetConversionDefinitionCommand,
            "conversion_definition_id",
            9,
        ),
        (
            "delete_conversion_from_transport",
            {"crm_user_id": 1, "app_id": 11, "conversion_definition_id": 9},
            DeleteConversionDefinitionCommand,
            "conversion_definition_id",
            9,
        ),
        (
            "get_param_from_transport",
            {"crm_user_id": 1, "app_id": 11, "param_definition_id": 5},
            GetParamDefinitionCommand,
            "param_definition_id",
            5,
        ),
        (
            "update_param_from_transport",
            {"crm_user_id": 1, "app_id": 11, "param_definition_id": 5, "label": "Campaign"},
            UpdateParamDefinitionCommand,
            "label",
            "Campaign",
        ),
        (
            "delete_param_from_transport",
            {"crm_user_id": 1, "app_id": 11, "param_definition_id": 5},
            DeleteParamDefinitionCommand,
            "param_definition_id",
            5,
        ),
        (
            "get_secret_template_from_transport",
            {"crm_user_id": 1, "app_id": 11, "template_id": 3},
            GetSecretTemplatesCommand,
            "template_id",
            3,
        ),
        (
            "update_secret_template_from_transport",
            {
                "crm_user_id": 1,
                "app_id": 11,
                "template_id": 3,
                "key": "api_key",
                "name": "API Key",
                "secret_type": "text",
                "visibility": "server_private",
            },
            UpdateSecretTemplateCommand,
            "template_id",
            3,
        ),
        (
            "delete_secret_template_from_transport",
            {"crm_user_id": 1, "app_id": 11, "template_id": 3},
            DeleteSecretTemplateCommand,
            "template_id",
            3,
        ),
        (
            "get_app_secret_from_transport",
            {"crm_user_id": 1, "app_id": 11, "app_secret_id": 13},
            GetAppSecretValueCommand,
            "app_secret_id",
            13,
        ),
        (
            "update_app_secret_from_transport",
            {"crm_user_id": 1, "app_id": 11, "secret_id": 13, "value": "updated-secret"},
            UpdateAppSecretCommand,
            "secret_id",
            13,
        ),
        (
            "delete_app_secret_from_transport",
            {"crm_user_id": 1, "app_id": 11, "secret_id": 13},
            DeleteAppSecretCommand,
            "secret_id",
            13,
        ),
        (
            "get_postback_from_transport",
            {"crm_user_id": 1, "app_id": 11, "postback_id": 17},
            GetPostbackRuleCommand,
            "postback_id",
            17,
        ),
        (
            "update_postback_from_transport",
            {"crm_user_id": 1, "app_id": 11, "postback_id": 17, "url": "https://example.com/pb"},
            UpdatePostbackRuleCommand,
            "url",
            "https://example.com/pb",
        ),
        (
            "delete_postback_from_transport",
            {"crm_user_id": 1, "app_id": 11, "postback_id": 17},
            DeletePostbackRuleCommand,
            "postback_id",
            17,
        ),
        (
            "get_push_campaign_from_transport",
            {"crm_user_id": 1, "app_id": 11, "push_id": 21},
            GetPushCampaignCommand,
            "push_id",
            21,
        ),
        (
            "update_push_campaign_from_transport",
            {"crm_user_id": 1, "app_id": 11, "push_id": 21, "title": "Updated Title"},
            UpdatePushCampaignCommand,
            "title",
            "Updated Title",
        ),
        (
            "delete_push_campaign_from_transport",
            {"crm_user_id": 1, "app_id": 11, "push_id": 21},
            DeletePushCampaignCommand,
            "push_id",
            21,
        ),
        (
            "start_push_campaign_from_transport",
            {"crm_user_id": 1, "app_id": 11, "push_id": 21},
            StartPushCampaignCommand,
            "push_id",
            21,
        ),
        (
            "share_app_access_from_transport",
            {"crm_user_id": 1, "app_id": 11, "manager_id": 99, "role_code": "manager"},
            ShareAppAccessCommand,
            "role_code",
            "manager",
        ),
        (
            "list_users_with_access_from_transport",
            {
                "crm_user_id": 1,
                "app_id": 11,
                "role_code": "manager",
                "limit": 50,
                "offset": 0,
                "search": "john",
            },
            ListUsersWithAccessCommand,
            "search",
            "john",
        ),
        (
            "delete_app_access_from_transport",
            {"crm_user_id": 1, "app_id": 11, "manager_id": 99},
            DeleteAppAccessCommand,
            "manager_id",
            99,
        ),
    ],
)
def test_admin_command_mapper_maps_new_route_commands(
    mapper_name: str,
    payload: dict[str, object],
    expected_type: type[object],
    expected_field: str,
    expected_value: object,
) -> None:
    command = getattr(AdminCommandMapper, mapper_name)(payload)

    assert isinstance(command, expected_type)
    assert getattr(command, expected_field) == expected_value
