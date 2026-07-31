from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from app.modules.crm.application.access_decorators import AuthorizationAwareService, require_permission
from app.modules.crm.application.admin.crm_authorization.protocol import CrmAuthorizationServiceProtocol
from app.modules.crm.application.admin.exception import ClickNotFound, InstallNotFound
from app.modules.crm.application.admin.push.commands import (
    CreatePushCampaignCommand,
    DeletePushCampaignCommand,
    GetPushCampaignCommand,
    ListPushCampaignsCommand,
    PushDeviceRegisterCommand,
    UpdatePushCampaignCommand,
)
from app.modules.crm.application.admin.push.exception import (
    InvalidScheduledAt,
    PushAppUserNotFound,
    PushCampaignAppMismatch,
    PushCampaignNotFound,
    PushPlatformNotFound,
)
from app.modules.crm.application.admin.push.mappers import PushCommandsMapper
from app.modules.crm.application.admin.push.protocol import PushServiceProtocol
from app.modules.crm.application.admin.push.responses import (
    CreatePushCampaignResponse,
    DeletePushCampaignResponse,
    GetPushCampaignResponse,
    ListPushCampaignResponse,
    RegisterDeviceResponse,
    UpdatePushCampaignResponse,
)
from app.modules.crm.application.attribution.protocol import CrmAttributionGateway
from app.modules.crm.application.mapper import PaginationMapper
from app.modules.crm.domain.param_definition.CrmParamDefinitionEntity import CrmParamDefinitionEntity, DefaultParamKeys
from app.modules.crm.domain.permission.CrmPermissionEntity import CrmPermissionEntity
from app.modules.crm.domain.push_campaign.CrmPushCampaignEntity import CrmPushCampaignEntity
from app.modules.crm.domain.push_token.CrmPushTokenEntity import CrmPushTokenEntity
from app.modules.crm.domain.uow import UnitOfWorkFactoryProtocol, UnitOfWorkProtocol


class PushService(PushServiceProtocol):
    def __init__(
        self,
        uow_factory: UnitOfWorkFactoryProtocol,
        authorization_service: CrmAuthorizationServiceProtocol,
        attribution_gateway: CrmAttributionGateway,
    ) -> None:
        self._uow_factory = uow_factory
        self._authorization_service = authorization_service
        self._attribution_gateway = attribution_gateway

    @staticmethod
    def _parse_scheduled_at(value: str | None) -> datetime | None:
        if value is None:
            return None

        try:
            return datetime.fromisoformat(value).astimezone(UTC)
        except ValueError as exc:
            raise InvalidScheduledAt(value) from exc

    @staticmethod
    def _get_push_campaign(
        uow: UnitOfWorkProtocol,
        *,
        push_id: int,
        app_id: int | None = None,
    ) -> CrmPushCampaignEntity:
        campaign = uow.push_campaign_repo.get_by_id(push_id)

        if campaign is None:
            raise PushCampaignNotFound(push_id)

        if app_id is not None and campaign.app_id != app_id:
            raise PushCampaignAppMismatch(push_id, app_id)

        return campaign

    def _resolve_campaign_access_context(
        _service: AuthorizationAwareService,
        uow: UnitOfWorkProtocol,
        command: Any,
    ) -> tuple[int | None, int | None]:
        """Resolve the app that owns a campaign before authorizing its deletion."""
        campaign = PushService._get_push_campaign(uow, push_id=command.push_id)
        return command.crm_user_id, campaign.app_id

    @require_permission(CrmPermissionEntity.manage_push_permission())
    def create(self, command: CreatePushCampaignCommand) -> CreatePushCampaignResponse:
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

        return CreatePushCampaignResponse(campaign=PushCommandsMapper.push_campaign_domain_to_value(saved_campaign))

    @require_permission(CrmPermissionEntity.manage_push_permission())
    def update(self, command: UpdatePushCampaignCommand) -> UpdatePushCampaignResponse:
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

        return UpdatePushCampaignResponse(campaign=PushCommandsMapper.push_campaign_domain_to_value(saved_campaign))

    @require_permission(
        CrmPermissionEntity.manage_push_permission(),
        context_resolver=_resolve_campaign_access_context,
    )
    def delete(self, command: DeletePushCampaignCommand) -> DeletePushCampaignResponse:
        with self._uow_factory.create() as uow:
            campaign = self._get_push_campaign(
                uow,
                push_id=command.push_id,
            )

            deleted_campaign = uow.push_campaign_repo.delete(command.push_id)

        return DeletePushCampaignResponse(campaign=PushCommandsMapper.push_campaign_domain_to_value(deleted_campaign))

    @require_permission(CrmPermissionEntity.manage_push_permission())
    def list(self, command: ListPushCampaignsCommand) -> ListPushCampaignResponse:
        with self._uow_factory.create() as uow:
            campaigns = uow.push_campaign_repo.list_by_app_id(
                command.app_id,
                pagination=PaginationMapper.pagination_from_command(command),
            )

        return ListPushCampaignResponse(
            campaigns=[PushCommandsMapper.push_campaign_domain_to_value(it) for it in campaigns]
        )

    @require_permission(CrmPermissionEntity.manage_push_permission())
    def get(self, command: GetPushCampaignCommand) -> GetPushCampaignResponse:
        with self._uow_factory.create() as uow:
            campaign = self._get_push_campaign(
                uow,
                push_id=command.push_id,
                app_id=command.app_id,
            )

        return GetPushCampaignResponse(campaign=PushCommandsMapper.push_campaign_domain_to_value(campaign))

    def register_device(self, command: PushDeviceRegisterCommand) -> RegisterDeviceResponse:
        click = self._attribution_gateway.get_click_context(command.click_id)
        if click is None:
            raise ClickNotFound(command.click_id)
        if click.install_id is None:
            raise InstallNotFound(command.click_id)

        with self._uow_factory.create() as uow:
            platform = uow.app_platform_repo.get_by_install_key(command.install_key)

            if platform is None or platform.platform_id is None:
                raise PushPlatformNotFound()

            app_user = None
            if command.app_user_id is not None:
                app_user = uow.app_user_repo.get_by_id(command.app_user_id)

                if app_user is None:
                    raise PushAppUserNotFound(command.app_user_id)

            definitions = uow.param_definition_repo.list_by_app_id(platform.app_id)

            filtered_payload = CrmParamDefinitionEntity.get_params_for_aggregation(
                params=command.params,
                params_dictionary=definitions,
            )

            geo = filtered_payload.get(DefaultParamKeys.GEO.value, None)
            country_code = filtered_payload.get(DefaultParamKeys.COUNTRY_CODE.value, None)
            lang = filtered_payload.get(DefaultParamKeys.LANG.value, None)

            entity = CrmPushTokenEntity(
                install_id=click.install_id,
                click_id=click.click_id,
                push_token=command.push_token,
                app_user_id=app_user.app_user_id if app_user is not None else None,
                geo=geo,
                lang=lang,
                country_code=country_code,
            )

            result = uow.push_token_repo.save(entity)

        return RegisterDeviceResponse()
