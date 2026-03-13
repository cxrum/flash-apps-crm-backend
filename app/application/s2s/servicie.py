from app.application.exceptions import ApplicationError
from app.application.s2s.commands import S2SClickCommand
from app.application.s2s.resposes import S2SClickResponse
from app.domain.app_platform.CrmAppPlatformEntity import CrmAppPlatformEntity
from app.domain.click.CrmClickEntity import CrmClickEntity
from app.domain.uow import CrmUnitOfWorkProtocol


class S2SService:
    def __init__(
        self,
        uow: CrmUnitOfWorkProtocol,
    ) -> None:
        self._uow = uow

    def _resolve_platform(
        self,
        platform: str,
        app_code: str,
        uow: CrmUnitOfWorkProtocol,
    ) -> CrmAppPlatformEntity | None:
        app = uow.app_repo.get_by_slug(app_code)
        if app is None:
            raise ApplicationError(f"Unknown app code: {app_code}")

        platform_entities = uow.app_platform_repo.list_by_app_id(app.app_id or 0)
        for platform_entity in platform_entities:
            if platform_entity.platform == platform:
                return platform_entity

        return None

    @staticmethod
    def _resolve_click_id(command: S2SClickCommand) -> str:
        raw_click_id = command.click_id or command.idempotency_key
        if raw_click_id is None or not raw_click_id.strip():
            raise ApplicationError("click_id or idempotency_key is required")
        return raw_click_id

    def process_click(self, command: S2SClickCommand) -> S2SClickResponse:
        with self._uow as uow:
            platform = self._resolve_platform(command.platform, command.app_code, uow)
            
            if platform is None:
                raise ApplicationError(
                    f"Platform {command.platform} is not configured for app {command.app_code}",
                )
            if platform.platform_id is None:
                raise ApplicationError("Platform repository returned entity without platform_id")

            click_id = self._resolve_click_id(command)
            
            new_click = CrmClickEntity(
                click_id=click_id,
                app_platform_id=platform.platform_id,
                ip_address=command.ip,
                user_agent=command.user_agent,
                redirect_target=command.redirect_url,
            )
            
            existing_click = uow.click_repo.get_by_id(click_id)
            new_click.accepted()
            
            if existing_click is not None:
                existing_click.validate_platform_match(platform.platform_id)
                new_click.set_new_click_id()
                new_click.duplicate()
            
            new_click.init_by_params(dict(command.params))
            new_click.validate_click_status()
            
            click = uow.click_repo.insert(
                new_click
            )

            return S2SClickResponse(click_id=click.click_id)
