from __future__ import annotations

import inspect
from typing import Any, get_args, get_origin, get_type_hints

from app.domain.crm import entities as crm_entities
from app.domain.contracts import repositories as crm_repositories
from app.domain.crm.app.CrmAppEntity import CrmAppEntity
from app.domain.crm.app_platform.CrmAppPlatformEntity import CrmAppPlatformEntity
from app.domain.crm.app_secret.CrmAppSecretEntity import CrmAppSecretEntity
from app.domain.crm.app_user.CrmAppUserEntity import CrmAppUserEntity
from app.domain.crm.click.CrmClickEntity import CrmClickEntity
from app.domain.crm.conversion_definition.CrmConversionDefinitionEntity import CrmConversionDefinitionEntity
from app.domain.crm.current_param.CrmCurrentParamEntity import CrmCurrentParamEntity
from app.domain.crm.event.CrmEventEntity import CrmEventEntity
from app.domain.crm.install.CrmInstallEntity import CrmInstallEntity
from app.domain.crm.metric_definition.CrmMetricDefinitionEntity import CrmMetricDefinitionEntity
from app.domain.crm.param_definition.CrmParamDefinitionEntity import CrmParamDefinitionEntity
from app.domain.crm.permission.CrmPermissionEntity import CrmPermissionEntity
from app.domain.crm.postback_rule.CrmPostbackRuleEntity import CrmPostbackRuleEntity
from app.domain.crm.push_campaign.CrmPushCampaignEntity import CrmPushCampaignEntity
from app.domain.crm.push_event.CrmPushEventEntity import CrmPushEventEntity
from app.domain.crm.push_token.CrmPushTokenEntity import CrmPushTokenEntity
from app.domain.crm.role.CrmRoleEntity import CrmRoleEntity
from app.domain.crm.role_permission.CrmRolePermissionEntity import CrmRolePermissionEntity
from app.domain.crm.secret_template.CrmSecretTemplateEntity import CrmSecretTemplateEntity
from app.domain.crm.user_app_access.CrmUserAppAccessEntity import CrmUserAppAccessEntity
from app.domain.crm.CrmUserEntity import CrmUserEntity
from app.domain.crm.user_role.CrmUserRoleEntity import CrmUserRoleEntity
from app.domain.crm.audit_log.CrmAuditLogEntity import (
    CrmAuditLogEntity,
)
from app.domain.contracts.repositories import (
    CrmAppPlatformRepositoryProtocol,
    CrmAppRepositoryProtocol,
    CrmAppSecretRepositoryProtocol,
    CrmAppUserRepositoryProtocol,
    CrmAuditLogRepositoryProtocol,
    CrmClickRepositoryProtocol,
    CrmConversionDefinitionRepositoryProtocol,
    CrmCurrentParamRepositoryProtocol,
    CrmEventRepositoryProtocol,
    CrmInstallRepositoryProtocol,
    CrmMetricDefinitionRepositoryProtocol,
    CrmParamDefinitionRepositoryProtocol,
    CrmPermissionRepositoryProtocol,
    CrmPostbackRuleRepositoryProtocol,
    CrmPushCampaignRepositoryProtocol,
    CrmPushEventRepositoryProtocol,
    CrmPushTokenRepositoryProtocol,
    CrmRolePermissionRepositoryProtocol,
    CrmRoleRepositoryProtocol,
    CrmSecretTemplateRepositoryProtocol,
    CrmUserAppAccessRepositoryProtocol,
    CrmUserRepositoryProtocol,
    CrmUserRoleRepositoryProtocol,
)


_SINGLE_WRITE_METHODS: list[tuple[type, str, type]] = [
    (CrmAppRepositoryProtocol, "save", CrmAppEntity),
    (CrmAppPlatformRepositoryProtocol, "save", CrmAppPlatformEntity),
    (CrmUserRepositoryProtocol, "save", CrmUserEntity),
    (CrmRoleRepositoryProtocol, "save", CrmRoleEntity),
    (CrmPermissionRepositoryProtocol, "save", CrmPermissionEntity),
    (CrmRolePermissionRepositoryProtocol, "save", CrmRolePermissionEntity),
    (CrmUserRoleRepositoryProtocol, "save", CrmUserRoleEntity),
    (CrmUserAppAccessRepositoryProtocol, "save", CrmUserAppAccessEntity),
    (CrmClickRepositoryProtocol, "insert", CrmClickEntity),
    (CrmAppUserRepositoryProtocol, "save", CrmAppUserEntity),
    (CrmInstallRepositoryProtocol, "save", CrmInstallEntity),
    (CrmEventRepositoryProtocol, "insert", CrmEventEntity),
    (CrmCurrentParamRepositoryProtocol, "save", CrmCurrentParamEntity),
    (CrmMetricDefinitionRepositoryProtocol, "save", CrmMetricDefinitionEntity),
    (CrmConversionDefinitionRepositoryProtocol, "save", CrmConversionDefinitionEntity),
    (CrmSecretTemplateRepositoryProtocol, "save", CrmSecretTemplateEntity),
    (CrmAppSecretRepositoryProtocol, "save", CrmAppSecretEntity),
    (CrmParamDefinitionRepositoryProtocol, "save", CrmParamDefinitionEntity),
    (CrmPostbackRuleRepositoryProtocol, "save", CrmPostbackRuleEntity),
    (CrmPushCampaignRepositoryProtocol, "save", CrmPushCampaignEntity),
    (CrmPushTokenRepositoryProtocol, "save", CrmPushTokenEntity),
    (CrmPushEventRepositoryProtocol, "insert", CrmPushEventEntity),
    (CrmAuditLogRepositoryProtocol, "insert", CrmAuditLogEntity),
]


_BATCH_WRITE_METHODS: list[tuple[type, str, type]] = [
    (CrmAppRepositoryProtocol, "save_many", CrmAppEntity),
    (CrmAppPlatformRepositoryProtocol, "save_many", CrmAppPlatformEntity),
    (CrmUserRepositoryProtocol, "save_many", CrmUserEntity),
    (CrmRoleRepositoryProtocol, "save_many", CrmRoleEntity),
    (CrmPermissionRepositoryProtocol, "save_many", CrmPermissionEntity),
    (CrmRolePermissionRepositoryProtocol, "save_many", CrmRolePermissionEntity),
    (CrmUserRoleRepositoryProtocol, "save_many", CrmUserRoleEntity),
    (CrmUserAppAccessRepositoryProtocol, "save_many", CrmUserAppAccessEntity),
    (CrmClickRepositoryProtocol, "insert_many", CrmClickEntity),
    (CrmAppUserRepositoryProtocol, "save_many", CrmAppUserEntity),
    (CrmInstallRepositoryProtocol, "save_many", CrmInstallEntity),
    (CrmEventRepositoryProtocol, "insert_many", CrmEventEntity),
    (CrmCurrentParamRepositoryProtocol, "save_many", CrmCurrentParamEntity),
    (CrmMetricDefinitionRepositoryProtocol, "save_many", CrmMetricDefinitionEntity),
    (CrmConversionDefinitionRepositoryProtocol, "save_many", CrmConversionDefinitionEntity),
    (CrmSecretTemplateRepositoryProtocol, "save_many", CrmSecretTemplateEntity),
    (CrmAppSecretRepositoryProtocol, "save_many", CrmAppSecretEntity),
    (CrmParamDefinitionRepositoryProtocol, "save_many", CrmParamDefinitionEntity),
    (CrmPostbackRuleRepositoryProtocol, "save_many", CrmPostbackRuleEntity),
    (CrmPushCampaignRepositoryProtocol, "save_many", CrmPushCampaignEntity),
    (CrmPushTokenRepositoryProtocol, "save_many", CrmPushTokenEntity),
    (CrmPushEventRepositoryProtocol, "insert_many", CrmPushEventEntity),
    (CrmAuditLogRepositoryProtocol, "insert_many", CrmAuditLogEntity),
]


def _get_first_non_self_annotation(protocol: type, method_name: str) -> Any:
    method = getattr(protocol, method_name)
    signature = inspect.signature(method)
    first_param = next(param for param in signature.parameters.values() if param.name != "self")
    type_hints = get_type_hints(
        method,
        globalns={**vars(crm_repositories), **vars(crm_entities)},
    )
    return type_hints[first_param.name]


def test_single_write_contracts_accept_domain_entities() -> None:
    for protocol, method_name, expected_entity_type in _SINGLE_WRITE_METHODS:
        annotation = _get_first_non_self_annotation(protocol, method_name)
        assert annotation is expected_entity_type


def test_batch_write_contracts_accept_lists_of_domain_entities() -> None:
    for protocol, method_name, expected_entity_type in _BATCH_WRITE_METHODS:
        annotation = _get_first_non_self_annotation(protocol, method_name)
        assert get_origin(annotation) is list
        (inner_type,) = get_args(annotation)
        assert inner_type is expected_entity_type


def test_immutable_log_contracts_expose_insert_only_for_writes() -> None:
    immutable_log_protocols = [
        CrmClickRepositoryProtocol,
        CrmEventRepositoryProtocol,
        CrmPushEventRepositoryProtocol,
        CrmAuditLogRepositoryProtocol,
    ]

    for protocol in immutable_log_protocols:
        assert hasattr(protocol, "insert")
        assert hasattr(protocol, "insert_many")
        assert not hasattr(protocol, "save")
        assert not hasattr(protocol, "save_many")
