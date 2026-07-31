from typing import Annotated

from fastapi import Depends

from app.core.bus.contract import IAsyncEventBus
from app.core.bus.di import get_in_memory_event_bus
from app.core.config import settings
from app.modules.crm.application.admin.audit.protocol import AuditServiceProtocol
from app.modules.crm.application.admin.audit.service import AuditService
from app.modules.crm.application.admin.crm_authorization.protocol import CrmAuthorizationServiceProtocol
from app.modules.crm.application.admin.crm_authorization.service import CrmAuthorizationService
from app.modules.crm.application.admin.definitions.protocol import DefinitionsServiceProtocol
from app.modules.crm.application.admin.definitions.service import DefinitionsService
from app.modules.crm.application.admin.secrets.protocol import SecretsServiceProtocol
from app.modules.crm.application.admin.secrets.service import SecretsService
from app.modules.crm.application.audited.audited_apps import AuditedAppsService
from app.modules.crm.application.contracts.encryption import EncryptionServiceProtocol
from app.modules.crm.application.contracts.ip2location import IP2LocationGatewayProtocol
from app.modules.crm.application.contracts.requester import S2SRequesterProtocol
from app.modules.crm.application.sdk.apps.protocol import AppServiceProtocol
from app.modules.crm.application.sdk.apps.service import AppService
from app.modules.crm.di.infra import get_uow_factory
from app.modules.crm.domain.hash_protocol import HashProtocol
from app.modules.crm.domain.uow import UnitOfWorkFactoryProtocol
from app.modules.crm.infra.services.encryption import EncryptionService
from app.modules.crm.infra.services.hashing import ServerHash
from app.modules.crm.infra.services.ip2location import IP2LocationGateway
from app.modules.crm.infra.services.s2s.request_builder import S2SRequester


def get_ip2location_gateway() -> IP2LocationGatewayProtocol:
    return IP2LocationGateway(settings.ip2location_bin_database_path)


def get_crm_authorization_service(
    uow_factory: Annotated[UnitOfWorkFactoryProtocol, Depends(get_uow_factory)],
) -> CrmAuthorizationServiceProtocol:
    return CrmAuthorizationService(uow_factory)


def get_admin_audit_service(
    uow_factory: Annotated[UnitOfWorkFactoryProtocol, Depends(get_uow_factory)],
    authorization_service: Annotated[CrmAuthorizationServiceProtocol, Depends(get_crm_authorization_service)],
) -> AuditServiceProtocol:
    return AuditService(uow_factory, authorization_service)


def get_s2s_requester() -> S2SRequesterProtocol:
    return S2SRequester()


def get_app_secrets_encryption_service() -> EncryptionServiceProtocol:
    return EncryptionService()


def get_admin_secrets_service(
    uow_factory: Annotated[UnitOfWorkFactoryProtocol, Depends(get_uow_factory)],
    authorization_service: Annotated[CrmAuthorizationServiceProtocol, Depends(get_crm_authorization_service)],
    encryption_service: Annotated[EncryptionServiceProtocol, Depends(get_app_secrets_encryption_service)],
) -> SecretsServiceProtocol:
    return SecretsService(uow_factory, authorization_service, encryption_service)


def get_admin_definitions_service(
    uow_factory: Annotated[UnitOfWorkFactoryProtocol, Depends(get_uow_factory)],
    user_service: Annotated[CrmAuthorizationServiceProtocol, Depends(get_crm_authorization_service)],
) -> DefinitionsServiceProtocol:
    return DefinitionsService(uow_factory, user_service)


def get_hash_service() -> HashProtocol:
    return ServerHash()


def get_sdk_app_service(
    uow_factory: Annotated[UnitOfWorkFactoryProtocol, Depends(get_uow_factory)],
    authorization_service: Annotated[CrmAuthorizationServiceProtocol, Depends(get_crm_authorization_service)],
    encryption_service: Annotated[EncryptionServiceProtocol, Depends(get_app_secrets_encryption_service)],
    hash_service: Annotated[HashProtocol, Depends(get_hash_service)],
    event_bus: Annotated[IAsyncEventBus, Depends(get_in_memory_event_bus)],
) -> AppServiceProtocol:
    app_service = AppService(uow_factory, event_bus, authorization_service, encryption_service, hash_service)
    return AuditedAppsService(uow_factory, app_service, event_bus)
