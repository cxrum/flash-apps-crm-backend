from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
from typing import Mapping, TypeVar

from pydantic import BaseModel

from app.application.admin.entities import (
    CreateAppCommand,
    CreateAppPlatformCommand,
    CreateConversionDefinitionCommand,
    CreateMetricDefinitionCommand,
    CreateParamDefinitionCommand,
    CreatePostbackRuleCommand,
    CreatePushCampaignCommand,
    CreateRoleCommand,
    CreateSecretTemplateCommand,
    GetAuditLogCommand,
    GetStatsCommand,
    ListAppPlatformsCommand,
    ListAppsCommand,
    ListAppSecretsCommand,
    ListClickLogsCommand,
    ListConversionDefinitionsCommand,
    ListEventLogsCommand,
    ListMetricDefinitionsCommand,
    ListParamDefinitionsCommand,
    ListPostbackRulesCommand,
    ListPushCampaignsCommand,
    ListRolesCommand,
    ListSecretTemplatesCommand,
    UpdateConversionDefinitionCommand,
    UpdateMetricDefinitionCommand,
    UpdateParamDefinitionCommand,
    UpdateSecretTemplateCommand,
    UpsertAppSecretsCommand,
)
from app.application.admin.responses import (
    AppSecretResponseEntry,
    AuditLogResponseEntry,
    ClickLogResponseEntry,
    ConversionDefinitionResponseEntry,
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
    MetricDefinitionResponseEntry,
    ParamDefinitionResponseEntry,
    RawEventLogResponseEntry,
    SecretTemplateResponseEntry,
    UpdateAppSecretResponse,
    UpdateConversionDefinitionResponse,
    UpdateMetricDefinitionResponse,
    UpdateParamDefinitionResponse,
)
from app.application.exceptions import ApplicationError
from app.domain.app_secret.CrmAppSecretEntity import CrmAppSecretEntity
from app.domain.audit_log.CrmAuditLogEntity import CrmAuditLogEntity
from app.domain.click.CrmClickEntity import CrmClickEntity
from app.domain.conversion_definition.CrmConversionDefinitionEntity import (
    CrmConversionDefinitionEntity,
)
from app.domain.events.CrmEventEntity import EventEntity
from app.domain.metric_definition.CrmMetricDefinitionEntity import CrmMetricDefinitionEntity
from app.domain.param_definition.CrmParamDefinitionEntity import CrmParamDefinitionEntity
from app.domain.secret_template.CrmSecretTemplateEntity import CrmSecretTemplateEntity

TCommand = TypeVar("TCommand", bound=BaseModel)


class AdminCommandMapper:
    @staticmethod
    def _to_command(command_type: type[TCommand], payload: Mapping[str, object]) -> TCommand:
        return command_type.model_validate(dict(payload))

    @classmethod
    def list_apps_from_transport(cls, payload: Mapping[str, object]) -> ListAppsCommand:
        return cls._to_command(ListAppsCommand, payload)

    @classmethod
    def create_app_from_transport(cls, payload: Mapping[str, object]) -> CreateAppCommand:
        return cls._to_command(CreateAppCommand, payload)

    @classmethod
    def list_app_platforms_from_transport(cls, payload: Mapping[str, object]) -> ListAppPlatformsCommand:
        return cls._to_command(ListAppPlatformsCommand, payload)

    @classmethod
    def create_app_platform_from_transport(cls, payload: Mapping[str, object]) -> CreateAppPlatformCommand:
        return cls._to_command(CreateAppPlatformCommand, payload)

    @classmethod
    def list_metrics_from_transport(cls, payload: Mapping[str, object]) -> ListMetricDefinitionsCommand:
        return cls._to_command(ListMetricDefinitionsCommand, payload)

    @classmethod
    def create_metric_from_transport(cls, payload: Mapping[str, object]) -> CreateMetricDefinitionCommand:
        return cls._to_command(CreateMetricDefinitionCommand, payload)

    @classmethod
    def list_conversions_from_transport(cls, payload: Mapping[str, object]) -> ListConversionDefinitionsCommand:
        return cls._to_command(ListConversionDefinitionsCommand, payload)

    @classmethod
    def create_conversion_from_transport(cls, payload: Mapping[str, object]) -> CreateConversionDefinitionCommand:
        return cls._to_command(CreateConversionDefinitionCommand, payload)

    @classmethod
    def list_params_from_transport(cls, payload: Mapping[str, object]) -> ListParamDefinitionsCommand:
        return cls._to_command(ListParamDefinitionsCommand, payload)

    @classmethod
    def create_param_from_transport(cls, payload: Mapping[str, object]) -> CreateParamDefinitionCommand:
        return cls._to_command(CreateParamDefinitionCommand, payload)

    @classmethod
    def list_secret_templates_from_transport(cls, payload: Mapping[str, object]) -> ListSecretTemplatesCommand:
        return cls._to_command(ListSecretTemplatesCommand, payload)

    @classmethod
    def create_secret_template_from_transport(cls, payload: Mapping[str, object]) -> CreateSecretTemplateCommand:
        return cls._to_command(CreateSecretTemplateCommand, payload)

    @classmethod
    def list_app_secrets_from_transport(cls, payload: Mapping[str, object]) -> ListAppSecretsCommand:
        return cls._to_command(ListAppSecretsCommand, payload)

    @classmethod
    def upsert_app_secrets_from_transport(cls, payload: Mapping[str, object]) -> UpsertAppSecretsCommand:
        return cls._to_command(UpsertAppSecretsCommand, payload)

    @classmethod
    def list_postbacks_from_transport(cls, payload: Mapping[str, object]) -> ListPostbackRulesCommand:
        return cls._to_command(ListPostbackRulesCommand, payload)

    @classmethod
    def create_postback_from_transport(cls, payload: Mapping[str, object]) -> CreatePostbackRuleCommand:
        return cls._to_command(CreatePostbackRuleCommand, payload)

    @classmethod
    def list_push_campaigns_from_transport(cls, payload: Mapping[str, object]) -> ListPushCampaignsCommand:
        return cls._to_command(ListPushCampaignsCommand, payload)

    @classmethod
    def create_push_campaign_from_transport(cls, payload: Mapping[str, object]) -> CreatePushCampaignCommand:
        return cls._to_command(CreatePushCampaignCommand, payload)

    @classmethod
    def stats_from_transport(cls, payload: Mapping[str, object]) -> GetStatsCommand:
        return cls._to_command(GetStatsCommand, payload)

    @classmethod
    def click_logs_from_transport(cls, payload: Mapping[str, object]) -> ListClickLogsCommand:
        return cls._to_command(ListClickLogsCommand, payload)

    @classmethod
    def event_logs_from_transport(cls, payload: Mapping[str, object]) -> ListEventLogsCommand:
        return cls._to_command(ListEventLogsCommand, payload)

    @classmethod
    def list_roles_from_transport(cls, payload: Mapping[str, object]) -> ListRolesCommand:
        return cls._to_command(ListRolesCommand, payload)

    @classmethod
    def create_role_from_transport(cls, payload: Mapping[str, object]) -> CreateRoleCommand:
        return cls._to_command(CreateRoleCommand, payload)

    @classmethod
    def audit_log_from_transport(cls, payload: Mapping[str, object]) -> GetAuditLogCommand:
        return cls._to_command(GetAuditLogCommand, payload)


class AdminDomainMapper:
    @staticmethod
    def _has_field(command: BaseModel, field_name: str) -> bool:
        return field_name in command.model_fields_set

    @staticmethod
    def _required_str(value: str | None, *, field_name: str) -> str:
        if value is None:
            raise ApplicationError(f"{field_name} is required")

        normalized = value.strip()
        if not normalized:
            raise ApplicationError(f"{field_name} is required")
        return normalized

    @staticmethod
    def _bool_or_default(value: bool | None, *, default: bool) -> bool:
        return default if value is None else value

    @classmethod
    def _patched_required_str(
        cls,
        command: BaseModel,
        *,
        field_name: str,
        current_value: str,
        label: str,
    ) -> str:
        if not cls._has_field(command, field_name):
            return current_value
        return cls._required_str(getattr(command, field_name), field_name=label)

    @classmethod
    def _patched_value(
        cls,
        command: BaseModel,
        *,
        field_name: str,
        current_value: object,
    ) -> object:
        if not cls._has_field(command, field_name):
            return current_value
        return getattr(command, field_name)

    @classmethod
    def _patched_bool(
        cls,
        command: BaseModel,
        *,
        field_name: str,
        current_value: bool,
    ) -> bool:
        if not cls._has_field(command, field_name):
            return current_value

        value = getattr(command, field_name)
        if value is None:
            return current_value
        return value

    @classmethod
    def _secret_template_scope(cls, visibility: str | None) -> str:
        normalized_visibility = cls._required_str(
            visibility,
            field_name="Secret visibility",
        ).lower()
        visibility_to_scope = {
            "global": "client_public",
            "client_public": "client_public",
            "private": "server_private",
            "server_private": "server_private",
        }
        scope = visibility_to_scope.get(normalized_visibility)
        if scope is None:
            raise ApplicationError("Secret visibility is invalid")
        return scope

    @staticmethod
    def metric_definition_from_command(
        command: CreateMetricDefinitionCommand,
    ) -> CrmMetricDefinitionEntity:
        return CrmMetricDefinitionEntity(
            machine_key=AdminDomainMapper._required_str(command.key, field_name="Metric key"),
            display_name=AdminDomainMapper._required_str(command.name, field_name="Metric name"),
            app_id=command.app_id,
            description=command.description,
            enabled=AdminDomainMapper._bool_or_default(command.is_active, default=True),
        )

    @classmethod
    def metric_definition_from_update_command(
        cls,
        entity: CrmMetricDefinitionEntity,
        command: UpdateMetricDefinitionCommand,
    ) -> CrmMetricDefinitionEntity:
        return replace(
            entity,
            machine_key=cls._patched_required_str(
                command,
                field_name="key",
                current_value=entity.machine_key,
                label="Metric key",
            ),
            display_name=cls._patched_required_str(
                command,
                field_name="name",
                current_value=entity.display_name,
                label="Metric name",
            ),
            description=cls._patched_value(
                command,
                field_name="description",
                current_value=entity.description,
            ),
            enabled=cls._patched_bool(
                command,
                field_name="is_active",
                current_value=entity.enabled,
            ),
        )

    @staticmethod
    def conversion_definition_from_command(
        command: CreateConversionDefinitionCommand,
    ) -> CrmConversionDefinitionEntity:
        revenue_enabled = getattr(command, "revenue_enabled", None)
        expects_amount = getattr(command, "expects_amount", None)
        expects_currency = getattr(command, "expects_currency", None)
        has_currency_contract = isinstance(command.currency, str) and command.currency.strip() != ""

        return CrmConversionDefinitionEntity(
            machine_key=AdminDomainMapper._required_str(command.key, field_name="Conversion key"),
            display_name=AdminDomainMapper._required_str(command.name, field_name="Conversion name"),
            app_id=command.app_id,
            description=command.description,
            revenue_enabled=AdminDomainMapper._bool_or_default(
                revenue_enabled,
                default=has_currency_contract,
            ),
            expects_amount=AdminDomainMapper._bool_or_default(
                expects_amount,
                default=has_currency_contract,
            ),
            expects_currency=AdminDomainMapper._bool_or_default(
                expects_currency,
                default=has_currency_contract,
            ),
            dedup_mode=command.dedup_mode or "none",
        )

    @classmethod
    def conversion_definition_from_update_command(
        cls,
        entity: CrmConversionDefinitionEntity,
        command: UpdateConversionDefinitionCommand,
    ) -> CrmConversionDefinitionEntity:
        dedup_mode = entity.dedup_mode
        if cls._has_field(command, "dedup_mode"):
            dedup_mode = cls._required_str(command.dedup_mode, field_name="Dedup mode")

        return replace(
            entity,
            machine_key=cls._patched_required_str(
                command,
                field_name="key",
                current_value=entity.machine_key,
                label="Conversion key",
            ),
            display_name=cls._patched_required_str(
                command,
                field_name="name",
                current_value=entity.display_name,
                label="Conversion name",
            ),
            description=cls._patched_value(
                command,
                field_name="description",
                current_value=entity.description,
            ),
            revenue_enabled=cls._patched_bool(
                command,
                field_name="revenue_enabled",
                current_value=entity.revenue_enabled,
            ),
            expects_amount=cls._patched_bool(
                command,
                field_name="expects_amount",
                current_value=entity.expects_amount,
            ),
            expects_currency=cls._patched_bool(
                command,
                field_name="expects_currency",
                current_value=entity.expects_currency,
            ),
            dedup_mode=dedup_mode,
        )

    @staticmethod
    def param_definition_from_command(
        command: CreateParamDefinitionCommand,
    ) -> CrmParamDefinitionEntity:
        return CrmParamDefinitionEntity(
            display_name=AdminDomainMapper._required_str(command.label, field_name="Param label"),
            machine_key=AdminDomainMapper._required_str(command.key, field_name="Param key"),
            data_type=AdminDomainMapper._required_str(command.param_type, field_name="Param type"),
            app_id=command.app_id,
            description=command.description,
            overwrite_policy=command.overwrite_policy or "replace",
            is_active=AdminDomainMapper._bool_or_default(command.is_active, default=True),
            visible_in_logs=AdminDomainMapper._bool_or_default(command.visible_in_logs, default=True),
            visible_in_stats=AdminDomainMapper._bool_or_default(command.visible_in_stats, default=False),
            filterable=AdminDomainMapper._bool_or_default(command.filterable, default=False),
            groupable=AdminDomainMapper._bool_or_default(command.groupable, default=False),
        )

    @classmethod
    def param_definition_from_update_command(
        cls,
        entity: CrmParamDefinitionEntity,
        command: UpdateParamDefinitionCommand,
    ) -> CrmParamDefinitionEntity:
        overwrite_policy = entity.overwrite_policy
        if cls._has_field(command, "overwrite_policy"):
            overwrite_policy = cls._required_str(
                command.overwrite_policy,
                field_name="Overwrite policy",
            )

        return replace(
            entity,
            display_name=cls._patched_required_str(
                command,
                field_name="label",
                current_value=entity.display_name,
                label="Param label",
            ),
            machine_key=cls._patched_required_str(
                command,
                field_name="key",
                current_value=entity.machine_key,
                label="Param key",
            ),
            data_type=cls._patched_required_str(
                command,
                field_name="param_type",
                current_value=entity.data_type,
                label="Param type",
            ),
            description=cls._patched_value(
                command,
                field_name="description",
                current_value=entity.description,
            ),
            overwrite_policy=overwrite_policy,
            is_active=cls._patched_bool(
                command,
                field_name="is_active",
                current_value=entity.is_active,
            ),
            visible_in_logs=cls._patched_bool(
                command,
                field_name="visible_in_logs",
                current_value=entity.visible_in_logs,
            ),
            visible_in_stats=cls._patched_bool(
                command,
                field_name="visible_in_stats",
                current_value=entity.visible_in_stats,
            ),
            filterable=cls._patched_bool(
                command,
                field_name="filterable",
                current_value=entity.filterable,
            ),
            groupable=cls._patched_bool(
                command,
                field_name="groupable",
                current_value=entity.groupable,
            ),
        )

    @staticmethod
    def secret_template_from_command(
        command: CreateSecretTemplateCommand,
    ) -> CrmSecretTemplateEntity:
        return CrmSecretTemplateEntity(
            code=AdminDomainMapper._required_str(command.key, field_name="Secret key"),
            display_name=AdminDomainMapper._required_str(command.name, field_name="Secret name"),
            scope=AdminDomainMapper._secret_template_scope(command.visibility),
            value_type=AdminDomainMapper._required_str(
                command.secret_type,
                field_name="Secret type",
            ),
        )
        
    @staticmethod
    def secret_template_from_update_command(
        command: UpdateSecretTemplateCommand,
    ) -> CrmSecretTemplateEntity:
        return CrmSecretTemplateEntity(
            template_id=command.template_id,
            code=AdminDomainMapper._required_str(command.key, field_name="Secret key"),
            display_name=AdminDomainMapper._required_str(command.name, field_name="Secret name"),
            scope=AdminDomainMapper._secret_template_scope(command.visibility),
            value_type=AdminDomainMapper._required_str(
                command.secret_type,
                field_name="Secret type",
            ),
        )


class AdminResponseMapper:
    @staticmethod
    def metric_definition_from_domain(entity: CrmMetricDefinitionEntity) -> MetricDefinitionResponseEntry:
        return MetricDefinitionResponseEntry(
            machine_key=entity.machine_key,
            display_name=entity.display_name,
            app_id=entity.app_id,
            description=entity.description,
            enabled=entity.enabled,
            visible_in_stats=entity.visible_in_stats,
            visible_in_logs=entity.visible_in_logs,
            metric_definition_id=entity.metric_definition_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    @classmethod
    def list_metric_definitions_from_domain(
        cls,
        entities: list[CrmMetricDefinitionEntity],
    ) -> ListMetricDefinitionsResponse:
        return ListMetricDefinitionsResponse(
            metric_definitions=[cls.metric_definition_from_domain(entity) for entity in entities],
        )

    @classmethod
    def create_metric_definition_from_domain(
        cls,
        entity: CrmMetricDefinitionEntity,
    ) -> CreateMetricDefinitionResponse:
        return CreateMetricDefinitionResponse(
            metric_definition=cls.metric_definition_from_domain(entity),
        )

    @classmethod
    def update_metric_definition_from_domain(
        cls,
        entity: CrmMetricDefinitionEntity,
    ) -> UpdateMetricDefinitionResponse:
        return UpdateMetricDefinitionResponse(
            metric_definition=cls.metric_definition_from_domain(entity),
        )

    @staticmethod
    def conversion_definition_from_domain(
        entity: CrmConversionDefinitionEntity,
    ) -> ConversionDefinitionResponseEntry:
        return ConversionDefinitionResponseEntry(
            machine_key=entity.machine_key,
            display_name=entity.display_name,
            app_id=entity.app_id,
            description=entity.description,
            revenue_enabled=entity.revenue_enabled,
            expects_amount=entity.expects_amount,
            expects_currency=entity.expects_currency,
            dedup_mode=entity.dedup_mode,
            conversion_definition_id=entity.conversion_definition_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    @classmethod
    def list_conversion_definitions_from_domain(
        cls,
        entities: list[CrmConversionDefinitionEntity],
    ) -> ListConversionDefinitionsResponse:
        return ListConversionDefinitionsResponse(
            conversion_definitions=[cls.conversion_definition_from_domain(entity) for entity in entities],
        )

    @classmethod
    def create_conversion_definition_from_domain(
        cls,
        entity: CrmConversionDefinitionEntity,
    ) -> CreateConversionDefinitionResponse:
        return CreateConversionDefinitionResponse(
            conversion_definition=cls.conversion_definition_from_domain(entity),
        )

    @classmethod
    def update_conversion_definition_from_domain(
        cls,
        entity: CrmConversionDefinitionEntity,
    ) -> UpdateConversionDefinitionResponse:
        return UpdateConversionDefinitionResponse(
            conversion_definition=cls.conversion_definition_from_domain(entity),
        )

    @staticmethod
    def param_definition_from_domain(entity: CrmParamDefinitionEntity) -> ParamDefinitionResponseEntry:
        return ParamDefinitionResponseEntry(
            display_name=entity.display_name,
            machine_key=entity.machine_key,
            data_type=entity.data_type,
            app_id=entity.app_id,
            description=entity.description,
            overwrite_policy=entity.overwrite_policy,
            is_active=entity.is_active,
            visible_in_logs=entity.visible_in_logs,
            visible_in_stats=entity.visible_in_stats,
            filterable=entity.filterable,
            groupable=entity.groupable,
            param_definition_id=entity.param_definition_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    @classmethod
    def list_param_definitions_from_domain(
        cls,
        entities: list[CrmParamDefinitionEntity],
    ) -> ListParamDefinitionsResponse:
        return ListParamDefinitionsResponse(
            param_definitions=[cls.param_definition_from_domain(entity) for entity in entities],
        )

    @classmethod
    def create_param_definition_from_domain(
        cls,
        entity: CrmParamDefinitionEntity,
    ) -> CreateParamDefinitionResponse:
        return CreateParamDefinitionResponse(
            param_definition=cls.param_definition_from_domain(entity),
        )

    @classmethod
    def update_param_definition_from_domain(
        cls,
        entity: CrmParamDefinitionEntity,
    ) -> UpdateParamDefinitionResponse:
        return UpdateParamDefinitionResponse(
            param_definition=cls.param_definition_from_domain(entity),
        )

    @staticmethod
    def secret_template_from_domain(entity: CrmSecretTemplateEntity) -> SecretTemplateResponseEntry:
        return SecretTemplateResponseEntry(
            code=entity.code,
            display_name=entity.display_name,
            scope=entity.scope,
            value_type=entity.value_type,
            is_masked=entity.is_masked,
            is_required=entity.is_required,
            template_id=entity.template_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    @classmethod
    def list_secret_templates_from_domain(
        cls,
        entities: list[CrmSecretTemplateEntity],
    ) -> ListSecretTemplatesResponse:
        return ListSecretTemplatesResponse(
            secret_templates=[cls.secret_template_from_domain(entity) for entity in entities],
        )

    @classmethod
    def create_secret_template_from_domain(
        cls,
        entity: CrmSecretTemplateEntity,
    ) -> CreateSecretTemplateResponse:
        return CreateSecretTemplateResponse(
            secret_template=cls.secret_template_from_domain(entity),
        )

    @staticmethod
    def app_secret_from_domain(entity: CrmAppSecretEntity) -> AppSecretResponseEntry:
        return AppSecretResponseEntry(
            template_id=entity.template_id,
            display_name="",
            value=entity.encrypted_value,
            platform_id=entity.platform_id,
            active_flag=entity.active_flag,
            version=entity.version,
            secret_id=entity.secret_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    @classmethod
    def list_app_secrets_from_domain(
        cls,
        entities: list[CrmAppSecretEntity],
    ) -> ListAppSecretsResponse:
        return ListAppSecretsResponse(
            app_secrets=[cls.app_secret_from_domain(entity) for entity in entities],
        )

    @classmethod
    def create_app_secret_from_domain(
        cls,
        entity: CrmAppSecretEntity,
    ) -> CreateAppSecretResponse:
        return CreateAppSecretResponse(
            app_secret=cls.app_secret_from_domain(entity),
        )

    @classmethod
    def update_app_secret_from_domain(
        cls,
        entity: CrmAppSecretEntity,
    ) -> UpdateAppSecretResponse:
        return UpdateAppSecretResponse(
            app_secret=cls.app_secret_from_domain(entity),
        )

    @staticmethod
    def click_log_from_domain(entity: CrmClickEntity) -> ClickLogResponseEntry:
        return ClickLogResponseEntry(
            click_id=entity.click_id,
            app_platform_id=entity.app_platform_id,
            status=entity.status,
            raw_query=deepcopy(entity.raw_query),
            ip_address=entity.ip_address,
            user_agent=entity.user_agent,
            geo=deepcopy(entity.geo),
            referrer=entity.referrer,
            source=entity.source,
            redirect_target=entity.redirect_target,
            normalized_params=deepcopy(entity.normalized_params),
            created_at=entity.created_at,
        )

    @classmethod
    def list_click_logs_from_domain(cls, entities: list[CrmClickEntity]) -> ListClickLogsResponse:
        return ListClickLogsResponse(
            clicks=[cls.click_log_from_domain(entity) for entity in entities],
        )

    @staticmethod
    def raw_event_from_domain(entity: EventEntity) -> RawEventLogResponseEntry:
        return RawEventLogResponseEntry(
            event_id=entity.event_id,
            click_id=entity.click_id,
            event_type=entity.event_type,
            event_key=entity.event_key,
            event_time_utc=entity.event_time_utc,
            app_user_id=entity.app_user_id,
            amount=entity.amount,
            currency=entity.currency,
            amount_usd=entity.amount_usd,
            payload=deepcopy(entity.payload),
            created_at=entity.created_at,
        )

    @classmethod
    def list_raw_events_from_domain(cls, entities: list[EventEntity]) -> ListRawEventsResponse:
        return ListRawEventsResponse(
            events=[cls.raw_event_from_domain(entity) for entity in entities],
        )

    @staticmethod
    def audit_log_from_domain(entity: CrmAuditLogEntity) -> AuditLogResponseEntry:
        return AuditLogResponseEntry(
            entity_changed=entity.entity_changed,
            user_id=entity.user_id,
            app_id=entity.app_id,
            entity_id=entity.entity_id,
            old_value=deepcopy(entity.old_value),
            new_value=deepcopy(entity.new_value),
            changed_at=entity.changed_at,
            audit_log_id=entity.audit_log_id,
        )

    @classmethod
    def list_audit_logs_from_domain(
        cls,
        entities: list[CrmAuditLogEntity],
    ) -> ListAuditLogsResponse:
        return ListAuditLogsResponse(
            audit_logs=[cls.audit_log_from_domain(entity) for entity in entities],
        )
