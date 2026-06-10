from __future__ import annotations

from app.application.access_decorators import require_app_access, require_permission
from app.application.admin.crm_authorization.protocol import CrmAuthorizationServiceProtocol
from app.application.admin.definitions.commands import (
    CreateConversionDefinitionCommand,
    CreateMetricDefinitionCommand,
    CreateParamDefinitionCommand,
    DeleteConversionDefinitionCommand,
    DeleteMetricDefinitionCommand,
    DeleteParamDefinitionCommand,
    GetConversionDefinitionCommand,
    GetMetricDefinitionCommand,
    GetParamDefinitionCommand,
    ListConversionDefinitionsCommand,
    ListMetricDefinitionsCommand,
    ListParamDefinitionsCommand,
    UpdateConversionDefinitionCommand,
    UpdateMetricDefinitionCommand,
    UpdateParamDefinitionCommand,
)
from app.application.admin.definitions.exceptions import (
    ConversionDefinitionNotFound,
    DefinitionAppMismatch,
    MetricDefinitionNotFound,
    ParamDefinitionNotFound,
)
from app.application.admin.definitions.mappers import DefinitionsResponseMapper
from app.application.admin.definitions.protocol import DefinitionsServiceProtocol
from app.application.admin.definitions.responses import (
    CreateConversionDefinitionResponse,
    CreateMetricDefinitionResponse,
    CreateParamDefinitionResponse,
    DeleteConversionDefinitionResponse,
    DeleteMetricDefinitionResponse,
    DeleteParamDefinitionResponse,
    GetConversionDefinitionResponse,
    GetMetricDefinitionResponse,
    GetParamDefinitionResponse,
    ListConversionDefinitionsResponse,
    ListMetricDefinitionsResponse,
    ListParamDefinitionsResponse,
    UpdateConversionDefinitionResponse,
    UpdateMetricDefinitionResponse,
    UpdateParamDefinitionResponse,
)
from app.application.mapper import PaginationMapper
from app.domain.conversion_definition.CrmConversionDefinitionEntity import (
    CrmConversionDefinitionEntity,
)
from app.domain.metric_definition.CrmMetricDefinitionEntity import CrmMetricDefinitionEntity
from app.domain.param_definition.CrmParamDefinitionEntity import CrmParamDefinitionEntity
from app.domain.permission.CrmPermissionEntity import CrmPermissionEntity
from app.domain.uow import UnitOfWorkFactoryProtocol, UnitOfWorkProtocol


class DefinitionsService(DefinitionsServiceProtocol):
    def __init__(
        self,
        uow_factory: UnitOfWorkFactoryProtocol,
        authorization_service: CrmAuthorizationServiceProtocol,
    ) -> None:
        self._uow_factory = uow_factory
        self._authorization_service = authorization_service

    @require_app_access()
    def list_metrics(
        self,
        command: ListMetricDefinitionsCommand,
    ) -> ListMetricDefinitionsResponse:
        with self._uow_factory.create() as uow:
            def_list = uow.metric_definition_repo.list_by_app_id(
                command.app_id,
                pagination=PaginationMapper.pagination_from_command(command),
            )

        return ListMetricDefinitionsResponse(
            metric_definitions=[DefinitionsResponseMapper.metric_domain_to_value(it) for it in def_list]
        )

    @staticmethod
    def _get_metric_definition(
        uow: UnitOfWorkProtocol,
        *,
        app_id: int,
        metric_definition_id: int,
    ) -> CrmMetricDefinitionEntity:
        definition = uow.metric_definition_repo.get_by_id(metric_definition_id)
        if definition is None:
            raise MetricDefinitionNotFound(metric_definition_id)
        if definition.app_id != app_id:
            raise DefinitionAppMismatch("Metric", app_id)

        return definition

    @require_app_access()
    def get_metric_definition(
        self,
        command: GetMetricDefinitionCommand,
    ) -> GetMetricDefinitionResponse:
        with self._uow_factory.create() as uow:
            metric = self._get_metric_definition(
                uow,
                app_id=command.app_id,
                metric_definition_id=command.metric_definition_id,
            )

        return GetMetricDefinitionResponse(
            metric_definition=DefinitionsResponseMapper.metric_domain_to_value(metric)
        )

    @require_permission(CrmPermissionEntity.edit_app_config_permission())
    def update_metric_definition(
        self,
        command: UpdateMetricDefinitionCommand,
    ) -> UpdateMetricDefinitionResponse:
        with self._uow_factory.create() as uow:
            definition = self._get_metric_definition(
                uow,
                app_id=command.app_id,
                metric_definition_id=command.metric_definition_id,
            )

            definition.update(
                machine_key=command.key,
                display_name=command.name,
                description=command.description,
                enabled=command.is_active,
            )

            saved_definition = uow.metric_definition_repo.save(definition)

        return UpdateMetricDefinitionResponse(
            metric_definition=DefinitionsResponseMapper.metric_domain_to_value(saved_definition)
        )

    @require_permission(CrmPermissionEntity.edit_app_config_permission())
    def delete_metric_definition(
        self,
        command: DeleteMetricDefinitionCommand,
    ) -> DeleteMetricDefinitionResponse:
        with self._uow_factory.create() as uow:
            definition = uow.metric_definition_repo.delete(command.metric_definition_id)

        return DeleteMetricDefinitionResponse(
            metric_definition=DefinitionsResponseMapper.metric_domain_to_value(definition)
        )

    @require_permission(CrmPermissionEntity.edit_app_config_permission())
    def create_metric_definition(
        self,
        command: CreateMetricDefinitionCommand,
    ) -> CreateMetricDefinitionResponse:
        entity = CrmMetricDefinitionEntity(
            machine_key=command.key,
            display_name=command.name,
            app_id=command.app_id,
            description=command.description,
            enabled=command.is_active,
        )

        with self._uow_factory.create() as uow:
            saved_definition = uow.metric_definition_repo.save(entity)

        return CreateMetricDefinitionResponse(
            metric_definition=DefinitionsResponseMapper.metric_domain_to_value(saved_definition)
        )

    @require_app_access()
    def list_conversions(
        self,
        command: ListConversionDefinitionsCommand,
    ) -> ListConversionDefinitionsResponse:
        with self._uow_factory.create() as uow:
            def_list = uow.conversion_definition_repo.list_by_app_id(
                command.app_id,
                pagination=PaginationMapper.pagination_from_command(command),
            )

        return ListConversionDefinitionsResponse(
            conversion_definitions=[DefinitionsResponseMapper.conversion_domain_to_value(it) for it in def_list]
        )

    @staticmethod
    def _get_conversion_definition(
        uow: UnitOfWorkProtocol,
        *,
        app_id: int,
        conversion_definition_id: int,
    ) -> CrmConversionDefinitionEntity:
        definition = uow.conversion_definition_repo.get_by_id(conversion_definition_id)
        if definition is None:
            raise ConversionDefinitionNotFound(conversion_definition_id)

        if definition.app_id != app_id:
            raise DefinitionAppMismatch("Conversion", app_id)

        return definition

    @require_app_access()
    def get_conversion_definition(
        self,
        command: GetConversionDefinitionCommand,
    ) -> GetConversionDefinitionResponse:
        with self._uow_factory.create() as uow:
            saved_definition = self._get_conversion_definition(
                uow,
                app_id=command.app_id,
                conversion_definition_id=command.conversion_definition_id,
            )

        return GetConversionDefinitionResponse(
            conversion_definition=DefinitionsResponseMapper.conversion_domain_to_value(saved_definition)
        )

    @require_permission(CrmPermissionEntity.edit_app_config_permission())
    def update_conversion_definition(
        self,
        command: UpdateConversionDefinitionCommand,
    ) -> UpdateConversionDefinitionResponse:
        with self._uow_factory.create() as uow:
            definition = self._get_conversion_definition(
                uow,
                app_id=command.app_id,
                conversion_definition_id=command.conversion_definition_id,
            )

            definition.update(
                machine_key=command.key,
                display_name=command.name,
                description=command.description,
                revenue_enabled=command.revenue_enabled,
                expects_amount=command.expects_amount,
                expects_currency=command.expects_currency,
                dedup_mode=command.dedup_mode,
            )

            saved_definition = uow.conversion_definition_repo.save(definition)

        return UpdateConversionDefinitionResponse(
            conversion_definition=DefinitionsResponseMapper.conversion_domain_to_value(saved_definition)
        )

    @require_permission(CrmPermissionEntity.edit_app_config_permission())
    def create_conversion_definition(
        self,
        command: CreateConversionDefinitionCommand,
    ) -> CreateConversionDefinitionResponse:
        entity = CrmConversionDefinitionEntity(
            machine_key=command.key,
            display_name=command.name,
            app_id=command.app_id,
            description=command.description,
            revenue_enabled=command.revenue_enabled,
            expects_amount=command.expects_amount,
            expects_currency=command.expects_currency,
            dedup_mode=command.dedup_mode or "none",
        )

        with self._uow_factory.create() as uow:
            saved_definition = uow.conversion_definition_repo.save(entity)

        return CreateConversionDefinitionResponse(
            conversion_definition=DefinitionsResponseMapper.conversion_domain_to_value(saved_definition)
        )

    @require_permission(CrmPermissionEntity.edit_app_config_permission())
    def delete_conversion_definition(
        self,
        command: DeleteConversionDefinitionCommand,
    ) -> DeleteConversionDefinitionResponse:
        with self._uow_factory.create() as uow:
            definition = uow.conversion_definition_repo.delete(command.conversion_definition_id)

        return DeleteConversionDefinitionResponse(
            conversion_definition=DefinitionsResponseMapper.conversion_domain_to_value(definition)
        )

    @require_app_access()
    def list_params(
        self,
        command: ListParamDefinitionsCommand,
    ) -> ListParamDefinitionsResponse:
        with self._uow_factory.create() as uow:
            def_list = uow.param_definition_repo.list_by_app_id(
                command.app_id,
                pagination=PaginationMapper.pagination_from_command(command),
            )

        return ListParamDefinitionsResponse(
            param_definitions=[DefinitionsResponseMapper.param_domain_to_value(it) for it in def_list]
        )

    @staticmethod
    def _get_param_definition(
        uow: UnitOfWorkProtocol,
        *,
        app_id: int,
        param_definition_id: int,
    ) -> CrmParamDefinitionEntity:
        definition = uow.param_definition_repo.get_by_id(param_definition_id)
        if definition is None:
            raise ParamDefinitionNotFound(param_definition_id)
        if definition.app_id != app_id:
            raise DefinitionAppMismatch("Param", app_id)

        return definition

    @require_app_access()
    def get_param_definition(
        self,
        command: GetParamDefinitionCommand,
    ) -> GetParamDefinitionResponse:
        with self._uow_factory.create() as uow:
            saved_definition = self._get_param_definition(
                uow,
                app_id=command.app_id,
                param_definition_id=command.param_definition_id,
            )

        return GetParamDefinitionResponse(
            param_definition=DefinitionsResponseMapper.param_domain_to_value(saved_definition)
        )

    @require_permission(CrmPermissionEntity.edit_app_config_permission())
    def update_param_definition(
        self,
        command: UpdateParamDefinitionCommand,
    ) -> UpdateParamDefinitionResponse:
        with self._uow_factory.create() as uow:
            definition = self._get_param_definition(
                uow,
                app_id=command.app_id,
                param_definition_id=command.param_definition_id,
            )
            definition.update(
                display_name=command.name,
                machine_key=command.key,
                data_type=command.data_type,
                description=command.description,
                overwrite_policy=command.overwrite_policy,
                is_active=command.is_active,
                visible_in_logs=command.visible_in_logs,
                visible_in_stats=command.visible_in_stats,
                filterable=command.filterable,
                groupable=command.groupable,
            )

            saved_definition = uow.param_definition_repo.save(definition)

        return UpdateParamDefinitionResponse(
            param_definition=DefinitionsResponseMapper.param_domain_to_value(saved_definition)
        )

    @require_permission(CrmPermissionEntity.edit_app_config_permission())
    def create_param_definition(
        self,
        command: CreateParamDefinitionCommand,
    ) -> CreateParamDefinitionResponse:
        entity = CrmParamDefinitionEntity(
            display_name=command.label,
            machine_key=command.key,
            data_type=command.param_type,
            app_id=command.app_id,
            description=command.description,
            overwrite_policy=command.overwrite_policy or "replace",
            is_active=command.is_active if command.is_active is not None else True,
            visible_in_logs=command.visible_in_logs if command.visible_in_logs is not None else True,
            visible_in_stats=command.visible_in_stats if command.visible_in_stats is not None else False,
            filterable=command.filterable if command.filterable is not None else False,
            groupable=command.groupable if command.groupable is not None else False,
        )

        with self._uow_factory.create() as uow:
            saved_definition = uow.param_definition_repo.save(entity)

        return CreateParamDefinitionResponse(
            param_definition=DefinitionsResponseMapper.param_domain_to_value(saved_definition)
        )

    @require_permission(CrmPermissionEntity.edit_app_config_permission())
    def delete_param_definition(
        self,
        command: DeleteParamDefinitionCommand,
    ) -> DeleteParamDefinitionResponse:
        with self._uow_factory.create() as uow:
            definition = uow.param_definition_repo.delete(command.param_definition_id)

        return DeleteParamDefinitionResponse(
            param_definition=DefinitionsResponseMapper.param_domain_to_value(definition)
        )
