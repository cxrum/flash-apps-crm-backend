from __future__ import annotations

from datetime import UTC, datetime

from app.application.admin.crm_authorization.service import CrmAuthorizationService
from app.application.admin.push.commands import (
    CreatePushCampaignCommand,
    DeletePushCampaignCommand,
    GetPushCampaignCommand,
    ListPushCampaignsCommand,
    PushDeviceRegisterCommand,
    UpdatePushCampaignCommand,
)
from app.application.admin.push.mappers import PushCommandsMapper
from app.application.admin.push.responses import (
    CreatePushCampaignResponse,
    DeletePushCampaignResponse,
    GetPushCampaignResponse,
    ListPushCampaignResponse,
    RegisterDeviceResponse,
    UpdatePushCampaignResponse,
)
from app.application.exceptions import ApplicationError
from app.application.mapper import PaginationMapper
from app.domain.param_definition.CrmParamDefinitionEntity import CrmParamDefinitionEntity, DefaultParamKeys
from app.domain.push_campaign.CrmPushCampaignEntity import CrmPushCampaignEntity
from app.domain.push_token import CrmPushTokenEntity
from app.domain.uow import UnitOfWorkFactoryProtocol, UnitOfWorkProtocol

class PushService:
    def __init__(
        self, 
        uow_factory: UnitOfWorkFactoryProtocol,
        authorization_service: CrmAuthorizationService, 
    ) -> None:
        self._uow_factory = uow_factory
        self._authorization_service = authorization_service
        
    @staticmethod
    def _parse_scheduled_at(value: str | None) -> datetime | None:
        if value is None:
            return None

        try:
            return datetime.fromisoformat(value).astimezone(UTC)
        except ValueError as exc:
            raise ApplicationError(f"Invalid scheduled_at value: {value}") from exc

    @staticmethod
    def _get_push_campaign(
        uow: UnitOfWorkProtocol,
        *,
        push_id: int,
        app_id: int | None = None,
    ) -> CrmPushCampaignEntity:
        campaign = uow.push_campaign_repo.get_by_id(push_id)

        if campaign is None:
            raise ApplicationError(f"Push campaign with id {push_id} doesn't exist")

        if app_id is not None and campaign.app_id != app_id:
            raise ApplicationError(f"App {app_id} doesn't exist")

        return campaign

    def create(self, command: CreatePushCampaignCommand) -> CreatePushCampaignResponse:
        self._authorization_service.check_user_app_access(
            crm_user_id=command.crm_user_id,
            app_id=command.app_id,
        )

        entity = CrmPushCampaignEntity(
            app_id=command.app_id,
            title=command.title,
            body=command.body,
            image_url=command.image_url,
            target_link=command.target_link,
            geo_filter=dict(command.geo_filter),
            scheduled_at=self._parse_scheduled_at(command.scheduled_at),
            status=command.status or "draft",
            created_by_user_id=command.crm_user_id,
        )

        with self._uow_factory.create() as uow:
            saved_campaign = uow.push_campaign_repo.save(entity)

        return CreatePushCampaignResponse(
            campaign=PushCommandsMapper.push_campaign_domain_to_value(saved_campaign)
        )

    def update(self, command: UpdatePushCampaignCommand) -> UpdatePushCampaignResponse:
        self._authorization_service.check_user_app_access(
            crm_user_id=command.crm_user_id,
            app_id=command.app_id,
        )

        with self._uow_factory.create() as uow:
            campaign = self._get_push_campaign(
                uow,
                push_id=command.campaign_id,
                app_id=command.app_id,
            )

            campaign.update(
                title=command.title,
                body=command.body,
                image_url=command.image_url,
                target_link=command.target_link,
                geo_filter=command.geo_filter,
                scheduled_at=self._parse_scheduled_at(command.scheduled_at),
                status=command.status,
            )

            saved_campaign = uow.push_campaign_repo.save(campaign)

        return UpdatePushCampaignResponse(
            campaign=PushCommandsMapper.push_campaign_domain_to_value(saved_campaign)
        )
    
    def delete(self, command: DeletePushCampaignCommand) -> DeletePushCampaignResponse:
        with self._uow_factory.create() as uow:
            campaign = self._get_push_campaign(
                uow,
                push_id=command.push_id,
            )

            self._authorization_service.check_user_app_access(
                crm_user_id=command.crm_user_id,
                app_id=campaign.app_id,
            )

            deleted_campaign = uow.push_campaign_repo.delete(command.push_id)

        return DeletePushCampaignResponse(
            campaign=PushCommandsMapper.push_campaign_domain_to_value(deleted_campaign)
        )
    
    def list(self, command: ListPushCampaignsCommand) -> ListPushCampaignResponse:
        self._authorization_service.check_user_app_access(
            crm_user_id=command.crm_user_id,
            app_id=command.app_id,
        )

        with self._uow_factory.create() as uow:
            campaigns = uow.push_campaign_repo.list_by_app_id(
                command.app_id,
                pagination=PaginationMapper.pagination_from_command(command),
            )

        return ListPushCampaignResponse(
            campaigns=[PushCommandsMapper.push_campaign_domain_to_value(it) for it in campaigns]
        )
    
    def get(self, command: GetPushCampaignCommand) -> GetPushCampaignResponse:
        self._authorization_service.check_user_app_access(
            crm_user_id=command.crm_user_id,
            app_id=command.app_id,
        )

        with self._uow_factory.create() as uow:
            campaign = self._get_push_campaign(
                uow,
                push_id=command.push_id,
                app_id=command.app_id,
            )

        return GetPushCampaignResponse(
            campaign=PushCommandsMapper.push_campaign_domain_to_value(campaign)
        )

    def register_device(self, command: PushDeviceRegisterCommand) -> RegisterDeviceResponse:
        with self._uow_factory.create() as uow:
            click = uow.click_repo.get_by_id(command.click_id)
            
            if click is None or click.click_id is None:
                raise ApplicationError()
            
            platform = uow.app_platform_repo.get_by_install_key(command.install_key)
            
            if platform is None or platform.platform_id is None:
                raise ApplicationError()
            
            install = uow.install_repo.get_by_click_id(command.click_id)
            if install is None or install.install_id is None:
                raise ApplicationError() 
            
            app_user = None
            if command.app_user_id is not None:
                app_user = uow.app_user_repo.get_by_id(command.app_user_id)
                
                if app_user is None:
                    raise ApplicationError
                
            definitions = uow.param_definition_repo.list_by_app_id(platform.app_id)
    
            filtered_payload = CrmParamDefinitionEntity.get_params_for_aggregation(
                params=command.params,
                params_dictionary=definitions,
            )
        
            geo = filtered_payload.get(DefaultParamKeys.GEO.value, None)
            country_code = filtered_payload.get(DefaultParamKeys.COUNTRY_CODE.value, None)
            lang = filtered_payload.get(DefaultParamKeys.LANG.value, None)
            
            entity = CrmPushTokenEntity(
                install_id = install.install_id,
                click_id = click.click_id,
                push_token = command.push_token,
                app_user_id = app_user.app_user_id if app_user is not None else None,
                geo = geo,
                lang=lang,
                country_code=country_code,
            )
            
            result = uow.push_token_repo.save(entity)
            
        return RegisterDeviceResponse()