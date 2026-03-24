from __future__ import annotations

from app.application.admin.crm_users.service import CrmUsersService
from app.application.admin.entities import (
    CreateConversionDefinitionCommand,
    CreateMetricDefinitionCommand,
    CreateParamDefinitionCommand,
    ListConversionDefinitionsCommand,
    ListMetricDefinitionsCommand,
    ListParamDefinitionsCommand,
    UpdateConversionDefinitionCommand,
    UpdateMetricDefinitionCommand,
    UpdateParamDefinitionCommand,
)
from app.application.admin.mappers import AdminDomainMapper, AdminResponseMapper
from app.application.admin.responses import (
    CreateConversionDefinitionResponse,
    CreateMetricDefinitionResponse,
    CreateParamDefinitionResponse,
    ListConversionDefinitionsResponse,
    ListMetricDefinitionsResponse,
    ListParamDefinitionsResponse,
    UpdateConversionDefinitionResponse,
    UpdateMetricDefinitionResponse,
    UpdateParamDefinitionResponse,
)
from app.application.exceptions import ApplicationError
from app.application.sdk.usecases.apps.service import AppService
from app.domain.conversion_definition.CrmConversionDefinitionEntity import (
    CrmConversionDefinitionEntity,
)
from app.domain.metric_definition.CrmMetricDefinitionEntity import CrmMetricDefinitionEntity
from app.domain.param_definition.CrmParamDefinitionEntity import CrmParamDefinitionEntity
from app.domain.uow import UnitOfWorkFacotyProtocol, UnitOfWorkProtocol


class DefenitionsService:
    def __init__(
        self,
        uow_factory: UnitOfWorkFacotyProtocol,
        user_service: CrmUsersService,
    ) -> None:
        self._uow_factory = uow_factory
        self._user_service = user_service

    def list_metrics(
        self,
        command: ListMetricDefinitionsCommand,
    ) -> ListMetricDefinitionsResponse:
        self._user_service.check_user_app_access(crm_user_id=command.crm_user_id, app_id=command.app_id)

        with self._uow_factory.create() as uow:
            def_list = uow.metric_definition_repo.list_by_app_id(command.app_id)

        return AdminResponseMapper.list_metric_definitions_from_domain(def_list)

    @staticmethod
    def _get_metric_definition(
        uow: UnitOfWorkProtocol,
        *,
        app_id: int,
        metric_definition_id: int,
    ) -> CrmMetricDefinitionEntity:
        definition = uow.metric_definition_repo.get_by_id(metric_definition_id)
        if definition is None:
            raise ApplicationError(f"Metric definition with id {metric_definition_id} doesnt exist")
        if definition.app_id != app_id:
            raise ApplicationError(
                f"App {app_id} doesnt exist",
            )
        return definition

    def get_metric_definition(
        self,
        command,
    ):
        ...

    
    def update_metric_defenition(
        self,
        command: UpdateMetricDefinitionCommand,
    ) -> UpdateMetricDefinitionResponse:
        self._user_service.check_user_app_access(crm_user_id=command.crm_user_id, app_id=command.app_id)

        with self._uow_factory.create() as uow:
            definition = self._get_metric_definition(
                uow,
                app_id=command.app_id,
                metric_definition_id=command.metric_definition_id,
            )
            updated_definition = AdminDomainMapper.metric_definition_from_update_command(
                definition,
                command,
            )
            saved_definition = uow.metric_definition_repo.save(updated_definition)

        return AdminResponseMapper.update_metric_definition_from_domain(saved_definition)
    
    def create_metric_defenition(
        self,
        command: CreateMetricDefinitionCommand,
    ) -> CreateMetricDefinitionResponse:
        self._user_service.check_user_app_access(crm_user_id=command.crm_user_id, app_id=command.app_id)
        entity = AdminDomainMapper.metric_definition_from_command(command)

        with self._uow_factory.create() as uow:
            AppService.ensure_app_exists(uow, command.app_id)
            saved_definition = uow.metric_definition_repo.save(entity)

        return AdminResponseMapper.create_metric_definition_from_domain(saved_definition)

    def list_conversions(
        self,
        command: ListConversionDefinitionsCommand,
    ) -> ListConversionDefinitionsResponse:
        self._user_service.check_user_app_access(crm_user_id=command.crm_user_id, app_id=command.app_id)

        with self._uow_factory.create() as uow:
            def_list = uow.conversion_definition_repo.list_by_app_id(command.app_id)

        return AdminResponseMapper.list_conversion_definitions_from_domain(def_list)

    @staticmethod
    def _get_conversion_definition(
        uow: UnitOfWorkProtocol,
        *,
        app_id: int,
        conversion_definition_id: int,
    ) -> CrmConversionDefinitionEntity:
        definition = uow.conversion_definition_repo.get_by_id(conversion_definition_id)
        if definition is None:
            raise ApplicationError(
                f"Conversion definition with id {conversion_definition_id} doesnt exist",
            )
        if definition.app_id != app_id:
            raise ApplicationError(
                f"App {app_id} doesnt exist",
            )
        return definition

    def update_conversion_defenition(
        self,
        command: UpdateConversionDefinitionCommand,
    ) -> UpdateConversionDefinitionResponse:
        self._user_service.check_user_app_access(crm_user_id=command.crm_user_id, app_id=command.app_id)

        with self._uow_factory.create() as uow:
            definition = self._get_conversion_definition(
                uow,
                app_id=command.app_id,
                conversion_definition_id=command.conversion_definition_id,
            )
            updated_definition = AdminDomainMapper.conversion_definition_from_update_command(
                definition,
                command,
            )
            saved_definition = uow.conversion_definition_repo.save(updated_definition)

        return AdminResponseMapper.update_conversion_definition_from_domain(saved_definition)
    
    def create_conversion_defenition(
        self,
        command: CreateConversionDefinitionCommand,
    ) -> CreateConversionDefinitionResponse:
        self._user_service.check_user_app_access(crm_user_id=command.crm_user_id, app_id=command.app_id)
        entity = AdminDomainMapper.conversion_definition_from_command(command)

        with self._uow_factory.create() as uow:
            AppService.ensure_app_exists(uow, command.app_id)
            saved_definition = uow.conversion_definition_repo.save(entity)

        return AdminResponseMapper.create_conversion_definition_from_domain(saved_definition)

    def list_params(
        self,
        command: ListParamDefinitionsCommand,
    ) -> ListParamDefinitionsResponse:
        self._user_service.check_user_app_access(crm_user_id=command.crm_user_id, app_id=command.app_id)

        with self._uow_factory.create() as uow:
            def_list = uow.param_definition_repo.list_by_app_id(command.app_id)

        return AdminResponseMapper.list_param_definitions_from_domain(def_list)

    @staticmethod
    def _get_param_definition(
        uow: UnitOfWorkProtocol,
        *,
        app_id: int,
        param_definition_id: int,
    ) -> CrmParamDefinitionEntity:
        definition = uow.param_definition_repo.get_by_id(param_definition_id)
        if definition is None:
            raise ApplicationError(f"Param definition with id {param_definition_id} doesnt exist")
        if definition.app_id != app_id:
            raise ApplicationError(
                f"App {app_id} doesnt exist",
            )
        return definition

    def update_param_defenition(
        self,
        command: UpdateParamDefinitionCommand,
    ) -> UpdateParamDefinitionResponse:
        self._user_service.check_user_app_access(crm_user_id=command.crm_user_id, app_id=command.app_id)

        with self._uow_factory.create() as uow:
            definition = self._get_param_definition(
                uow,
                app_id=command.app_id,
                param_definition_id=command.param_definition_id,
            )
            updated_definition = AdminDomainMapper.param_definition_from_update_command(
                definition,
                command,
            )
            saved_definition = uow.param_definition_repo.save(updated_definition)

        return AdminResponseMapper.update_param_definition_from_domain(saved_definition)
    
    def create_param_defenition(
        self,
        command: CreateParamDefinitionCommand,
    ) -> CreateParamDefinitionResponse:
        self._user_service.check_user_app_access(crm_user_id=command.crm_user_id, app_id=command.app_id)
        entity = AdminDomainMapper.param_definition_from_command(command)

        with self._uow_factory.create() as uow:
            AppService.ensure_app_exists(uow, command.app_id)
            saved_definition = uow.param_definition_repo.save(entity)

        return AdminResponseMapper.create_param_definition_from_domain(saved_definition)
