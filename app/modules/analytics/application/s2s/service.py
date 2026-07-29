from app.modules.analytics.application.s2s.commands import S2SClickCommand
from app.modules.analytics.application.s2s.exception import (
    PlatformNotConfigured,
    ResolvedPlatformInvalid,
    SignatureMismatch,
    UnknownAppCode,
)
from app.modules.analytics.application.s2s.protocol import ClickServiceProtocol
from app.modules.analytics.application.s2s.responses import S2SClickResponse
from app.modules.analytics.application.tracking.entities import TrackingRedirectCommand
from app.modules.analytics.application.tracking.responses import TrackingRedirectResponse
from app.modules.analytics.domain.uow import AnalyticsUnitOfWorkFactoryProtocol, AnalyticsUnitOfWorkProtocol
from app.modules.crm.application.contracts.ip2location import IP2LocationGatewayProtocol, IpLocation
from app.modules.crm.domain.app_platform.CrmAppPlatformEntity import CrmAppPlatformEntity
from app.modules.analytics.domain.click.AnalyticsClickEntity import AnalyticsClickEntity
from app.modules.crm.domain.hash_protocol import HashableValue
from app.modules.crm.domain.signature_protocol import SignatureProtocol


class ClickService(ClickServiceProtocol):
    def __init__(
        self,
        uow_factory: AnalyticsUnitOfWorkFactoryProtocol,
        signature_service: SignatureProtocol,
        ip2location_gateway: IP2LocationGatewayProtocol,
    ) -> None:
        self._uow_factory = uow_factory
        self._signature_service = signature_service
        self._ip2location_gateway = ip2location_gateway

    def _resolve_platform(
        self,
        platform: str,
        app_code: str,
        uow: AnalyticsUnitOfWorkProtocol,
    ) -> CrmAppPlatformEntity | None:
        app = uow.app_repo.get_by_slug(app_code)
        if app is None:
            raise UnknownAppCode(app_code)

        platform_entities = uow.app_platform_repo.list_by_app_id(app.app_id or 0)
        for platform_entity in platform_entities:
            if platform_entity.platform == platform:
                return platform_entity

        return None

    def _process_click(
        self,
        uow: AnalyticsUnitOfWorkProtocol,
        *,
        click: AnalyticsClickEntity,
        platform: CrmAppPlatformEntity,
        source_click_id: str | None = None,
    ) -> AnalyticsClickEntity:

        param_definitions = uow.param_definition_repo.list_by_app_id(platform.app_id)

        if platform.platform_id is None:
            raise ResolvedPlatformInvalid()

        click.validate_platform_match(platform.platform_id)
        click.normalize_params(param_definitions)

        if source_click_id is None:
            click.accepted()
        else:
            existed_click = uow.click_repo.get_by_id(source_click_id)
            if existed_click is None:
                click.accepted()
            else:
                click.duplicate()

        click.validate_click_status()

        click = uow.click_repo.insert(click)

        return click

    def process_s2s_click(self, command: S2SClickCommand) -> S2SClickResponse:
        with self._uow_factory.create() as uow:
            platform = self._resolve_platform(command.platform, command.app_code, uow)

            if platform is None:
                raise PlatformNotConfigured(command.platform, command.app_code)
            if platform.platform_id is None:
                raise PlatformNotConfigured(command.platform, command.app_code)

            is_signature_correct = self._signature_service.compare(
                value=HashableValue.from_str(command.raw_params),
                signature=HashableValue.from_hex(command.signature),
                key=platform.sdk_secret_encrypted,
            )

            if not is_signature_correct:
                raise SignatureMismatch()

            click = AnalyticsClickEntity(
                click_id=AnalyticsClickEntity.generate_click_id(),
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
                platform=platform,
                source_click_id=command.click_id,
            )

            return S2SClickResponse(click_id=click.click_id)

    def process_redirect_click(self, command: TrackingRedirectCommand) -> TrackingRedirectResponse:
        with self._uow_factory.create() as uow:
            platform = self._resolve_platform(command.platform, command.app_code, uow)

            if platform is None or platform.platform_id is None:
                raise PlatformNotConfigured(command.platform, command.app_code)

            click = AnalyticsClickEntity(
                click_id=AnalyticsClickEntity.generate_click_id(),
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
                platform=platform,
            )

            return TrackingRedirectResponse(click_id=click.click_id)
