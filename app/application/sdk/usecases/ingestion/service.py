from __future__ import annotations

from datetime import UTC, datetime

from app.application.exceptions import ApplicationLevelError
from app.application.sdk.entities import SdkInstallCommand
from app.application.sdk.event import MetricsEventBuilder
from app.application.sdk.usecases.ingestion.responses import SdkInstallResponse
from app.domain.click.CrmClickEntity import CrmClickEntity
from app.domain.events.CrmEventEntity import EventEntity
from app.domain.install.CrmInstallEntity import CrmInstallEntity
from app.domain.uow import CrmUnitOfWorkProtocol


class InsegisntionService:
    def __init__(
        self,
        uow: CrmUnitOfWorkProtocol,
    ) -> None:
        self._uow = uow

    @staticmethod
    def _generated_click_id(command: SdkInstallCommand) -> str:
        return f"{command.idempotency_key}"

    def _resolve_platform_id(self, install_key: str) -> int:
        platform = self._uow.app_platform_repo.get_by_install_key(install_key)
        
        if platform is None or platform.platform_id is None:
            raise ApplicationLevelError(f"Unknown install_key: {install_key}")
        
        return platform.platform_id

    def _resolve_click(self, command: SdkInstallCommand, app_platform_id: int) -> CrmClickEntity:
        click_id = command.click_id or self._generated_click_id(command)
        existing = self._uow.click_repo.get_by_id(click_id)
        
        if existing is not None:
            if existing.app_platform_id != app_platform_id:
                raise ApplicationLevelError(
                    f"Click {click_id} belongs to another platform",
                )
            return existing

        return self._uow.click_repo.insert(
            CrmClickEntity(
                click_id=click_id,
                app_platform_id=app_platform_id,
                raw_query=dict(command.params),
                normalized_params=dict(command.params),
                source="sdk_install",
            )
        )

    def process_install(self, command: SdkInstallCommand) -> SdkInstallResponse:
        app_platform_id = self._resolve_platform_id(command.install_key)
        click = self._resolve_click(command, app_platform_id)

        saved_install = self._uow.install_repo.save(
            CrmInstallEntity(
                click_id=click.click_id,
                app_platform_id=app_platform_id,
                device_data=command.device.model_dump(mode="python"),
            )
        )
        
        event = (
            MetricsEventBuilder(
                event_id=command.idempotency_key,
                click_id=click.click_id,
                event_key="install",
                app_user_id=saved_install.app_user_id
                )
            ._set_payload(
                    {
                        "install_key": command.install_key,
                        "params": dict(command.params),
                        "device": command.device.model_dump(mode="python"),
                    }
                )
            .build()    
        )
        
        self._uow.event_repo.insert(event)
        
        return SdkInstallResponse(
            click_id=click.click_id, 
            app_user_id=saved_install.app_user_id
        )
