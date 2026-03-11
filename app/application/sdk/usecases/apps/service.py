from dataclasses import dataclass
from datetime import datetime

from app.application.sdk.entities import SdkApplicationConfigurationCommand, SdkCreateAppCommand, SdkCreateAppPlatformCommand
from app.application.exceptions import ApplicationLevelError
from app.application.sdk.mappers import SdkDomainMapper
from app.application.sdk.usecases.apps.responses import AppConfigQueryResponse, CreateAppResponse, CreatePlatformResponse
from app.domain.uow import CrmUnitOfWorkProtocol


class AppService:
    def __init__(self, uow: CrmUnitOfWorkProtocol) -> None:
        self._uow = uow

    def create_app(self, command: SdkCreateAppCommand) -> CreateAppResponse:
        app = SdkDomainMapper.app_from_command(command)
        app.draft()
        
        with self._uow as uow:
            saved_app = uow.app_repo.save(app)
            
        if saved_app.app_id is None:
            raise ApplicationLevelError("App repository returned entity without app_id")
        
        return CreateAppResponse(app_id=saved_app.app_id)

    def create_platform(self, command: SdkCreateAppPlatformCommand) -> CreatePlatformResponse:
        platform_app = SdkDomainMapper.app_platform_from_command(command)
        
        if not platform_app.is_valid_platform():
            raise ApplicationLevelError("App platform does not valid")
        
        with self._uow as uow:    
            app = uow.app_repo.get_by_id(platform_app.app_id)
            
            if app is None:
                raise ApplicationLevelError(f"App with id {platform_app.app_id} doesnt exist")
        
            saved_platform_app = uow.app_platform_repo.save(platform_app)
            
        if saved_platform_app.platform_id is None:
            raise ApplicationLevelError("App platfrom repository returned empty entity")
        
        return CreatePlatformResponse(platform_id=saved_platform_app.platform_id)
    
    
    def get_app_config(self, command: SdkApplicationConfigurationCommand) -> AppConfigQueryResponse:
        raise NotImplementedError
