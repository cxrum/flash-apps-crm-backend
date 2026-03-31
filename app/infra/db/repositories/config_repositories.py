from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.app_secret.CrmAppSecretEntity import CrmAppSecretEntity
from app.domain.app_secret.app_secret_repository_protocol import CrmAppSecretRepositoryProtocol
from app.domain.conversion_definition.CrmConversionDefinitionEntity import CrmConversionDefinitionEntity
from app.domain.conversion_definition.conversion_definition_repository_protocol import (
    CrmConversionDefinitionRepositoryProtocol,
)
from app.domain.metric_definition.CrmMetricDefinitionEntity import CrmMetricDefinitionEntity
from app.domain.metric_definition.metric_definition_repository_protocol import (
    CrmMetricDefinitionRepositoryProtocol,
)
from app.domain.param_definition.CrmParamDefinitionEntity import CrmParamDefinitionEntity
from app.domain.param_definition.param_definition_repository_protocol import (
    CrmParamDefinitionRepositoryProtocol,
)
from app.domain.postback_rule.CrmPostbackRuleEntity import CrmPostbackRuleEntity
from app.domain.postback_rule.postback_rule_repository_protocol import CrmPostbackRuleRepositoryProtocol
from app.domain.postback_rule.template import PostbackTemplateEntity
from app.domain.secret_template.CrmSecretTemplateEntity import CrmSecretTemplateEntity
from app.domain.secret_template.secret_template_repository_protocol import (
    CrmSecretTemplateRepositoryProtocol,
)
from app.domain.pagination import Pagination
from app.infra.db.apps.models import AppPlatform
from app.infra.db.config.models import (
    AppSecret,
    ConversionDefinition,
    MetricDefinition,
    ParamDefinition,
    PostbackRule,
    SecretTemplate,
)


def _apply_pagination(stmt, pagination: Pagination | None):
    if pagination is not None and pagination.offset is not None:
        stmt = stmt.offset(pagination.offset)
    if pagination is not None and pagination.limit is not None:
        stmt = stmt.limit(pagination.limit)
    return stmt


class SqlAlchemyCrmMetricDefinitionRepository(CrmMetricDefinitionRepositoryProtocol):
    def __init__(self, session: Session) -> None:
        self.session = session

    def _to_domain(self, row: MetricDefinition) -> CrmMetricDefinitionEntity:
        return CrmMetricDefinitionEntity(
            metric_definition_id=row.metric_definition_id,
            app_id=row.app_id,
            machine_key=row.machine_key,
            display_name=row.display_name,
            description=row.description,
            enabled=row.enabled,
            visible_in_stats=row.visible_in_stats,
            visible_in_logs=row.visible_in_logs,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )

    def _to_row(self, entity: CrmMetricDefinitionEntity) -> MetricDefinition:
        kwargs: dict[str, object] = {
            "app_id": entity.app_id,
            "machine_key": entity.machine_key,
            "display_name": entity.display_name,
            "description": entity.description,
            "enabled": entity.enabled,
            "visible_in_stats": entity.visible_in_stats,
            "visible_in_logs": entity.visible_in_logs,
        }
        if entity.metric_definition_id is not None:
            kwargs["metric_definition_id"] = entity.metric_definition_id
        if entity.created_at is not None:
            kwargs["created_at"] = entity.created_at
        if entity.updated_at is not None:
            kwargs["updated_at"] = entity.updated_at
        return MetricDefinition(**kwargs)

    def save(self, entity: CrmMetricDefinitionEntity) -> CrmMetricDefinitionEntity:
        row = self.session.merge(self._to_row(entity))
        self.session.flush()
        return self._to_domain(row)

    def save_many(self, entities: list[CrmMetricDefinitionEntity]) -> list[CrmMetricDefinitionEntity]:
        rows = [self.session.merge(self._to_row(entity)) for entity in entities]
        self.session.flush()
        return [self._to_domain(row) for row in rows]

    def get_by_id(self, metric_definition_id: int) -> CrmMetricDefinitionEntity | None:
        row = self.session.get(MetricDefinition, metric_definition_id)
        return self._to_domain(row) if row is not None else None

    def delete(self, metric_definition_id: int) -> CrmMetricDefinitionEntity:
        row = self.session.get(MetricDefinition, metric_definition_id)
        if row is None:
            raise RuntimeError()

        metric_definition = self._to_domain(row)
        self.session.delete(row)
        self.session.flush()
        return metric_definition

    def list_by_app_id(
        self,
        app_id: int | None,
        *,
        pagination: Pagination | None = None,
    ) -> list[CrmMetricDefinitionEntity]:
        rows = self.session.scalars(_apply_pagination(
            select(MetricDefinition)
            .where(MetricDefinition.app_id == app_id)
            .order_by(MetricDefinition.metric_definition_id.asc()),
            pagination,
        )).all()
        return [self._to_domain(row) for row in rows]


class SqlAlchemyCrmConversionDefinitionRepository(CrmConversionDefinitionRepositoryProtocol):
    def __init__(self, session: Session) -> None:
        self.session = session

    def _to_domain(self, row: ConversionDefinition) -> CrmConversionDefinitionEntity:
        return CrmConversionDefinitionEntity(
            conversion_definition_id=row.conversion_definition_id,
            app_id=row.app_id,
            machine_key=row.machine_key,
            display_name=row.display_name,
            description=row.description,
            revenue_enabled=row.revenue_enabled,
            expects_amount=row.expects_amount,
            expects_currency=row.expects_currency,
            dedup_mode=row.dedup_mode,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )

    def _to_row(self, entity: CrmConversionDefinitionEntity) -> ConversionDefinition:
        kwargs: dict[str, object] = {
            "app_id": entity.app_id,
            "machine_key": entity.machine_key,
            "display_name": entity.display_name,
            "description": entity.description,
            "revenue_enabled": entity.revenue_enabled,
            "expects_amount": entity.expects_amount,
            "expects_currency": entity.expects_currency,
            "dedup_mode": entity.dedup_mode,
        }
        if entity.conversion_definition_id is not None:
            kwargs["conversion_definition_id"] = entity.conversion_definition_id
        if entity.created_at is not None:
            kwargs["created_at"] = entity.created_at
        if entity.updated_at is not None:
            kwargs["updated_at"] = entity.updated_at
        return ConversionDefinition(**kwargs)

    def save(self, entity: CrmConversionDefinitionEntity) -> CrmConversionDefinitionEntity:
        row = self.session.merge(self._to_row(entity))
        self.session.flush()
        return self._to_domain(row)

    def save_many(self, entities: list[CrmConversionDefinitionEntity]) -> list[CrmConversionDefinitionEntity]:
        rows = [self.session.merge(self._to_row(entity)) for entity in entities]
        self.session.flush()
        return [self._to_domain(row) for row in rows]

    def get_by_id(self, conversion_definition_id: int) -> CrmConversionDefinitionEntity | None:
        row = self.session.get(ConversionDefinition, conversion_definition_id)
        return self._to_domain(row) if row is not None else None

    def delete(self, conversion_definition_id: int) -> CrmConversionDefinitionEntity:
        row = self.session.get(ConversionDefinition, conversion_definition_id)
        if row is None:
            raise RuntimeError()

        conversion_definition = self._to_domain(row)
        self.session.delete(row)
        self.session.flush()
        return conversion_definition

    def list_by_app_id(
        self,
        app_id: int | None,
        *,
        pagination: Pagination | None = None,
    ) -> list[CrmConversionDefinitionEntity]:
        rows = self.session.scalars(_apply_pagination(
            select(ConversionDefinition)
            .where(ConversionDefinition.app_id == app_id)
            .order_by(ConversionDefinition.conversion_definition_id.asc()),
            pagination,
        )).all()
        return [self._to_domain(row) for row in rows]


class SqlAlchemyCrmParamDefinitionRepository(CrmParamDefinitionRepositoryProtocol):
    def __init__(self, session: Session) -> None:
        self.session = session

    def _to_domain(self, row: ParamDefinition) -> CrmParamDefinitionEntity:
        return CrmParamDefinitionEntity(
            param_definition_id=row.param_definition_id,
            app_id=row.app_id,
            display_name=row.display_name,
            description=row.description,
            machine_key=row.machine_key,
            data_type=row.data_type,
            overwrite_policy=row.overwrite_policy,
            is_active=row.is_active,
            visible_in_logs=row.visible_in_logs,
            visible_in_stats=row.visible_in_stats,
            filterable=row.filterable,
            groupable=row.groupable,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )

    def _to_row(self, entity: CrmParamDefinitionEntity) -> ParamDefinition:
        kwargs: dict[str, object] = {
            "app_id": entity.app_id,
            "display_name": entity.display_name,
            "description": entity.description,
            "machine_key": entity.machine_key,
            "data_type": entity.data_type,
            "overwrite_policy": entity.overwrite_policy,
            "is_active": entity.is_active,
            "visible_in_logs": entity.visible_in_logs,
            "visible_in_stats": entity.visible_in_stats,
            "filterable": entity.filterable,
            "groupable": entity.groupable,
        }
        if entity.param_definition_id is not None:
            kwargs["param_definition_id"] = entity.param_definition_id
        if entity.created_at is not None:
            kwargs["created_at"] = entity.created_at
        if entity.updated_at is not None:
            kwargs["updated_at"] = entity.updated_at
        return ParamDefinition(**kwargs)

    def save(self, entity: CrmParamDefinitionEntity) -> CrmParamDefinitionEntity:
        row = self.session.merge(self._to_row(entity))
        self.session.flush()
        return self._to_domain(row)

    def save_many(self, entities: list[CrmParamDefinitionEntity]) -> list[CrmParamDefinitionEntity]:
        rows = [self.session.merge(self._to_row(entity)) for entity in entities]
        self.session.flush()
        return [self._to_domain(row) for row in rows]

    def get_by_id(self, param_definition_id: int) -> CrmParamDefinitionEntity | None:
        row = self.session.get(ParamDefinition, param_definition_id)
        return self._to_domain(row) if row is not None else None

    def delete(self, param_definition_id: int) -> CrmParamDefinitionEntity:
        row = self.session.get(ParamDefinition, param_definition_id)
        if row is None:
            raise RuntimeError()

        param_definition = self._to_domain(row)
        self.session.delete(row)
        self.session.flush()
        return param_definition

    def list_by_app_id(
        self,
        app_id: int | None,
        *,
        pagination: Pagination | None = None,
    ) -> list[CrmParamDefinitionEntity]:
        rows = self.session.scalars(_apply_pagination(
            select(ParamDefinition)
            .where(ParamDefinition.app_id == app_id)
            .order_by(ParamDefinition.param_definition_id.asc()),
            pagination,
        )).all()
        return [self._to_domain(row) for row in rows]


class SqlAlchemyCrmSecretTemplateRepository(CrmSecretTemplateRepositoryProtocol):
    def __init__(self, session: Session) -> None:
        self.session = session

    def _to_domain(self, row: SecretTemplate) -> CrmSecretTemplateEntity:
        return CrmSecretTemplateEntity(
            template_id=row.template_id,
            code=row.code,
            display_name=row.display_name,
            scope=row.scope,
            value_type=row.value_type,
            is_masked=row.is_masked,
            is_required=row.is_required,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )

    def _to_row(self, entity: CrmSecretTemplateEntity) -> SecretTemplate:
        kwargs: dict[str, object] = {
            "code": entity.code,
            "display_name": entity.display_name,
            "scope": entity.scope,
            "value_type": entity.value_type,
            "is_masked": entity.is_masked,
            "is_required": entity.is_required,
        }
        if entity.template_id is not None:
            kwargs["template_id"] = entity.template_id
        if entity.created_at is not None:
            kwargs["created_at"] = entity.created_at
        if entity.updated_at is not None:
            kwargs["updated_at"] = entity.updated_at
        return SecretTemplate(**kwargs)

    def save(self, entity: CrmSecretTemplateEntity) -> CrmSecretTemplateEntity:
        row = self.session.merge(self._to_row(entity))
        self.session.flush()
        return self._to_domain(row)

    def save_many(self, entities: list[CrmSecretTemplateEntity]) -> list[CrmSecretTemplateEntity]:
        rows = [self.session.merge(self._to_row(entity)) for entity in entities]
        self.session.flush()
        return [self._to_domain(row) for row in rows]

    def get_by_id(self, template_id: int) -> CrmSecretTemplateEntity | None:
        row = self.session.get(SecretTemplate, template_id)
        return self._to_domain(row) if row is not None else None

    def delete(self, template_id: int) -> CrmSecretTemplateEntity:
        row = self.session.get(SecretTemplate, template_id)
        if row is None:
            raise RuntimeError()

        template = self._to_domain(row)
        self.session.delete(row)
        self.session.flush()
        return template

    def get_by_code(self, code: str) -> CrmSecretTemplateEntity | None:
        row = self.session.scalars(
            select(SecretTemplate).where(SecretTemplate.code == code)
        ).first()
        return self._to_domain(row) if row is not None else None

    def list_all(self, *, pagination: Pagination | None = None) -> list[CrmSecretTemplateEntity]:
        rows = self.session.scalars(_apply_pagination(
            select(SecretTemplate).order_by(SecretTemplate.template_id.asc()),
            pagination,
        )).all()
        return [self._to_domain(row) for row in rows]


class SqlAlchemyCrmPostbackRuleRepository(CrmPostbackRuleRepositoryProtocol):
    def __init__(self, session: Session) -> None:
        self.session = session

    def _to_domain(self, row: PostbackRule) -> CrmPostbackRuleEntity:
        return CrmPostbackRuleEntity(
            rule_id=row.rule_id,
            platform_app_id=row.platfrom_app_id,
            name=row.name,
            endpoint_url=row.endpoint_url,
            http_method=row.http_method,
            headers=dict(row.headers),
            auth_params=dict(row.auth_params),
            timeout=row.timeout,
            event_key=row.event_key,
            trigger_type=row.trigger_type,
            template=PostbackTemplateEntity.from_dict(row.template),
            retry_policy=dict(row.retry_policy),
            is_active=row.is_active,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )

    def _to_row(self, entity: CrmPostbackRuleEntity) -> PostbackRule:
        kwargs: dict[str, object] = {
            "platfrom_app_id": entity.platform_app_id,
            "name": entity.name,
            "endpoint_url": entity.endpoint_url,
            "http_method": entity.http_method,
            "headers": dict(entity.headers),
            "auth_params": dict(entity.auth_params),
            "timeout": entity.timeout,
            "event_key": entity.event_key,
            "trigger_type": entity.trigger_type,
            "template": dict(entity.template),
            "retry_policy": dict(entity.retry_policy),
            "is_active": entity.is_active,
        }
        if entity.rule_id is not None:
            kwargs["rule_id"] = entity.rule_id
        if entity.created_at is not None:
            kwargs["created_at"] = entity.created_at
        if entity.updated_at is not None:
            kwargs["updated_at"] = entity.updated_at
        return PostbackRule(**kwargs)

    def save(self, entity: CrmPostbackRuleEntity) -> CrmPostbackRuleEntity:
        row = self.session.merge(self._to_row(entity))
        self.session.flush()
        return self._to_domain(row)

    def save_many(self, entities: list[CrmPostbackRuleEntity]) -> list[CrmPostbackRuleEntity]:
        rows = [self.session.merge(self._to_row(entity)) for entity in entities]
        self.session.flush()
        return [self._to_domain(row) for row in rows]

    def get_by_id(self, rule_id: int) -> CrmPostbackRuleEntity | None:
        row = self.session.get(PostbackRule, rule_id)
        return self._to_domain(row) if row is not None else None

    def delete(self, rule_id: int) -> CrmPostbackRuleEntity:
        row = self.session.get(PostbackRule, rule_id)
        if row is None:
            raise RuntimeError()

        rule = self._to_domain(row)
        self.session.delete(row)
        self.session.flush()
        return rule

    def list_by_filters(
        self,
        *,
        rule_id: int | None = None,
        platfrom_app_id: int | None = None,
        name: str | None = None,
        endpoint_url: str | None = None,
        trigger_type: str | None = None,
        http_method: str | None = None,
        headers: dict[str, object] | None = None,
        auth_params: dict[str, str] | None = None,
        timeout: int | None = None,
        event_key: str | None = None,
        template: dict[str, object] | None = None,
        retry_policy: dict[str, object] | None = None,
        is_active: bool | None = None,
        updated_at: datetime | None = None,
        created_at: datetime | None = None,
        pagination: Pagination | None = None,
    ) -> list[CrmPostbackRuleEntity]:
        filter_values = {
            "rule_id": rule_id,
            "platfrom_app_id": platfrom_app_id,
            "name": name,
            "endpoint_url": endpoint_url,
            "trigger_type": trigger_type,
            "http_method": http_method,
            "headers": headers,
            "auth_params": auth_params,
            "timeout": timeout,
            "event_key": event_key,
            "template": template,
            "retry_policy": retry_policy,
            "is_active": is_active,
            "updated_at": updated_at,
            "created_at": created_at,
        }

        stmt = select(PostbackRule)
        for field_name, value in filter_values.items():
            if value is not None:
                stmt = stmt.where(getattr(PostbackRule, field_name) == value)

        rows = self.session.scalars(_apply_pagination(
            stmt.order_by(PostbackRule.rule_id.asc()),
            pagination,
        )).all()
        return [self._to_domain(row) for row in rows]

    def list_by_app_id(
        self,
        app_id: int,
        *,
        pagination: Pagination | None = None,
    ) -> list[CrmPostbackRuleEntity]:
        rows = self.session.scalars(_apply_pagination(
            select(PostbackRule)
            .join(AppPlatform, PostbackRule.platfrom_app_id == AppPlatform.platform_id)
            .where(AppPlatform.app_id == app_id)
            .order_by(PostbackRule.rule_id.asc()),
            pagination,
        )).all()
        return [self._to_domain(row) for row in rows]

    def list_active_by_app(
        self,
        app_id: int,
        *,
        pagination: Pagination | None = None,
    ) -> list[CrmPostbackRuleEntity]:
        rows = self.session.scalars(_apply_pagination(
            select(PostbackRule)
            .join(AppPlatform, PostbackRule.platfrom_app_id == AppPlatform.platform_id)
            .where(AppPlatform.app_id == app_id, PostbackRule.is_active.is_(True))
            .order_by(PostbackRule.rule_id.asc()),
            pagination,
        )).all()
        return [self._to_domain(row) for row in rows]


class SqlAlchemyCrmAppSecretRepository(CrmAppSecretRepositoryProtocol):
    def __init__(self, session: Session) -> None:
        self.session = session

    def _to_domain(self, row: AppSecret) -> CrmAppSecretEntity:
        return CrmAppSecretEntity(
            secret_id=row.secret_id,
            platform_id=row.platform_id,
            template_id=row.template_id,
            encrypted_value=row.encrypted_value,
            active_flag=row.active_flag,
            version=row.version,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )

    def _to_row(self, entity: CrmAppSecretEntity) -> AppSecret:
        kwargs: dict[str, object] = {
            "platform_id": entity.platform_id,
            "template_id": entity.template_id,
            "encrypted_value": entity.encrypted_value,
            "active_flag": entity.active_flag,
            "version": entity.version,
        }
        if entity.secret_id is not None:
            kwargs["secret_id"] = entity.secret_id
        if entity.created_at is not None:
            kwargs["created_at"] = entity.created_at
        if entity.updated_at is not None:
            kwargs["updated_at"] = entity.updated_at
        return AppSecret(**kwargs)

    def save(self, entity: CrmAppSecretEntity) -> CrmAppSecretEntity:
        row = self.session.merge(self._to_row(entity))
        self.session.flush()
        return self._to_domain(row)

    def save_many(self, entities: list[CrmAppSecretEntity]) -> list[CrmAppSecretEntity]:
        rows = [self.session.merge(self._to_row(entity)) for entity in entities]
        self.session.flush()
        return [self._to_domain(row) for row in rows]

    def get_by_id(self, secret_id: int) -> CrmAppSecretEntity | None:
        row = self.session.get(AppSecret, secret_id)
        return self._to_domain(row) if row is not None else None

    def delete(self, secret_id: int) -> CrmAppSecretEntity:
        row = self.session.get(AppSecret, secret_id)
        if row is None:
            raise RuntimeError()

        secret = self._to_domain(row)
        self.session.delete(row)
        self.session.flush()
        return secret

    def list_by_app_id(
        self,
        app_id: int,
        *,
        platform_id: int | None = None,
        pagination: Pagination | None = None,
    ) -> list[CrmAppSecretEntity]:
        stmt = (
            select(AppSecret)
            .join(AppPlatform, AppSecret.platform_id == AppPlatform.platform_id)
            .where(AppPlatform.app_id == app_id)
            .order_by(AppSecret.secret_id.asc())
        )
        
        if platform_id is not None:
            stmt = stmt.where(AppSecret.platform_id == platform_id)
            
        rows = self.session.scalars(_apply_pagination(stmt, pagination)).all()
        
        return [self._to_domain(row) for row in rows]

    def list_active_by_app(
        self,
        app_id: int,
        *,
        platform_id: int | None = None,
        pagination: Pagination | None = None,
    ) -> list[CrmAppSecretEntity]:
        stmt = (
            select(AppSecret)
            .join(AppPlatform, AppSecret.platform_id == AppPlatform.platform_id)
            .where(AppPlatform.app_id == app_id, AppSecret.active_flag.is_(True))
            .order_by(AppSecret.secret_id.asc())
        )
        if platform_id is not None:
            stmt = stmt.where(AppSecret.platform_id == platform_id)
        rows = self.session.scalars(_apply_pagination(stmt, pagination)).all()
        return [self._to_domain(row) for row in rows]
