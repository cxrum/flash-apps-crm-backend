from app.application.admin.crm_authorization.service import CrmAuthorizationService
from app.domain.uow import UnitOfWorkFactoryProtocol


class PushService:
    def __init__(
        self, 
        uow_factory: UnitOfWorkFactoryProtocol,
        authorization_service: CrmAuthorizationService, 
    ) -> None:
        self._uow_factory = uow_factory
        self._authorization_service = authorization_service
        
    def create(self, command): ...

    