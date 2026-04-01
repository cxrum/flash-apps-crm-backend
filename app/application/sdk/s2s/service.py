from collections.abc import Callable

from app.application.contracts.ip2location import IP2LocationGatewayProtocol, IpLocation
from app.application.exceptions import ApplicationError
from app.application.sdk.s2s.commands import S2SClickCommand
from app.application.sdk.s2s.responses import S2SClickResponse
from app.application.tracking.entities import TrackingRedirectCommand
from app.application.tracking.responses import TrackingRedirectResponse
from app.domain.app_platform.CrmAppPlatformEntity import CrmAppPlatformEntity
from app.domain.click.CrmClickEntity import CrmClickEntity
from app.domain.hash_protocol import HashedValue
from app.domain.param_definition.CrmParamDefinitionEntity import CrmParamDefinitionEntity
from app.domain.signature_protocol import SignatureProtocol
from app.domain.uow import UnitOfWorkFactoryProtocol, UnitOfWorkProtocol


class ClickService:
    def __init__(
        self,
        uow_factory: UnitOfWorkFactoryProtocol,
        signature_service: SignatureProtocol,
        ip2location_gateway: IP2LocationGatewayProtocol
    ) -> None:
        self._uow_factory = uow_factory
        self._signature_service = signature_service
        self._ip2location_gateway = ip2location_gateway

    def _resolve_platform(
        self,
        platform: str,
        app_code: str,
        uow: UnitOfWorkProtocol,
    ) -> CrmAppPlatformEntity | None:
        app = uow.app_repo.get_by_slug(app_code)
        if app is None:
            raise ApplicationError(f"Unknown app code: {app_code}")

        platform_entities = uow.app_platform_repo.list_by_app_id(app.app_id or 0)
        for platform_entity in platform_entities:
            if platform_entity.platform == platform:
                return platform_entity

        return None

    def _process_click(self, uow: UnitOfWorkProtocol, *, click: CrmClickEntity, platform: CrmAppPlatformEntity) -> CrmClickEntity:
        
        param_definitions = uow.param_definition_repo.list_by_app_id(platform.app_id)
                    
        if platform.platform_id is None:
            raise ApplicationError()
        
        click.validate_platform_match(platform.platform_id)
        click.normalize_params(param_definitions)
        
        if click.click_id is None:
            click.accepted()
        else:
            existed_click = uow.click_repo.get_by_id(click.click_id)
            if existed_click is None:
                raise ApplicationError("Click doesn't exist")
            
            click.duplicate()
        
        click.validate_click_status()
        
        click = uow.click_repo.insert(
            click
        )

        return click
    
    def process_s2s_click(self, command: S2SClickCommand) -> S2SClickResponse:
        with self._uow_factory.create() as uow:
            platform = self._resolve_platform(command.platform, command.app_code, uow)
            
            if platform is None:
                raise ApplicationError(
                    f"Platform {command.platform} is not configured for app {command.app_code}",
                )
            if platform.platform_id is None:
                raise ApplicationError("Platform repository returned entity without platform_id")
            
            is_signature_correct = self._signature_service.compare(
                value=HashedValue.from_str(command.raw_params),
                signature=HashedValue.from_hex(command.signature),
                key=platform.sdk_secret_hash
            )
            
            if not is_signature_correct:
                raise ApplicationError
            
            
            click = CrmClickEntity(
                click_id=CrmClickEntity.generate_click_id(),
                app_platform_id=platform.platform_id,
                ip_address=command.ip,
                user_agent=command.user_agent,
                redirect_target=command.redirect_url,
                raw_query=command.params,
            )
            
            location_data: IpLocation | None = None
            if command.ip is not None:
                location_data = self._ip2location_gateway.resolve(command.ip)
                
                click.city = location_data.city
                click.country_code = location_data.country_code
                click.language = location_data.language
                click.region = location_data.region
                
            click = self._process_click(
                uow,
                click=click,
                platform=platform
            )

            return S2SClickResponse(click_id=click.click_id)

    def process_redirect_click(self, command: TrackingRedirectCommand) -> TrackingRedirectResponse:
        with self._uow_factory.create() as uow:
            platform = self._resolve_platform(command.platform, command.app_code, uow)
            
            if platform is None:
                raise ApplicationError(
                    f"Platform {command.platform} is not configured for app {command.app_code}",
                )
            if platform.platform_id is None:
                raise ApplicationError("Platform repository returned entity without platform_id")
            
            
            click = CrmClickEntity(
                click_id=CrmClickEntity.generate_click_id(),
                app_platform_id=platform.platform_id,
                ip_address=command.ip,
                user_agent=command.user_agent,
                redirect_target=command.redirect_url,
                raw_query=command.params,
            )
            
            location_data: IpLocation | None = None
            if command.ip is not None:
                location_data = self._ip2location_gateway.resolve(command.ip)
                
                click.city = location_data.city
                click.country_code = location_data.country_code
                click.language = location_data.language
                click.region = location_data.region
                
            click = self._process_click(
                uow,
                click=click,
                platform=platform
            )

            return TrackingRedirectResponse(click_id=click.click_id)
    