from fastapi import Depends

from app.application.admin.crm_authorization.service import CrmAuthorizationService
from app.application.admin.definitions.service import DefinitionsService
from app.application.admin.logs.service import LogsService
from app.application.admin.postback.service import PostbackService
from app.application.admin.push.service import PushService
from app.application.admin.secrets.service import SecretsService
from app.application.contracts.encryption import EncryptionServiceProtocol
from app.application.contracts.ip2location import IP2LocationGatewayProtocol
from app.application.contracts.requester import S2SRequesterProtocol
from app.application.sdk.apps.service import AppService
from app.application.sdk.ingestion.service import IngestionService
from app.application.sdk.s2s.service import ClickService
from app.core.config import settings
from app.di.event_bus import get_in_memory_event_bus
from app.di.infra import get_uow_factory
from app.domain.currency.currency_convertor_protocol import (
    CurrencyConvertorClientProtocol,
)
from app.domain.event_bus.service_protocol import IAsyncEventBus
from app.domain.hash_protocol import HashProtocol
from app.domain.signature_protocol import SignatureProtocol
from app.domain.uow import UnitOfWorkFactoryProtocol
from app.infra.services.currency import CurrencyConvertorClient
from app.infra.services.encryption import EncryptionService
from app.infra.services.hashing import ServerHash
from app.infra.services.ip2location import IP2LocationGateway
from app.infra.services.s2s.request_builder import S2SRequester
from app.infra.services.signature import SignatureSHA256


def get_signature_sha256_service() -> SignatureProtocol:
    return SignatureSHA256()


def get_ip2location_gateway() -> IP2LocationGatewayProtocol:
    return IP2LocationGateway(settings.ip2location_bin_database_path)


def get_s2s_service(
    uow_factory: UnitOfWorkFactoryProtocol = Depends(get_uow_factory),
    signature_service: SignatureProtocol = Depends(get_signature_sha256_service),
    ip2location_gateway: IP2LocationGatewayProtocol = Depends(get_ip2location_gateway),
) -> ClickService:
    return ClickService(uow_factory, signature_service, ip2location_gateway)


def get_crm_authorization_service(
    uow_factory: UnitOfWorkFactoryProtocol = Depends(get_uow_factory),
) -> CrmAuthorizationService:
    return CrmAuthorizationService(uow_factory)


def get_push_service(
    uow_factory: UnitOfWorkFactoryProtocol = Depends(get_uow_factory),
    authorization_service: CrmAuthorizationService = Depends(
        get_crm_authorization_service
    ),
) -> PushService:
    return PushService(
        uow_factory=uow_factory, authorization_service=authorization_service
    )


def get_admin_logs_service(
    uow_factory: UnitOfWorkFactoryProtocol = Depends(get_uow_factory),
    authorization_service: CrmAuthorizationService = Depends(
        get_crm_authorization_service
    ),
) -> LogsService:
    return LogsService(uow_factory, authorization_service)


def get_s2s_requester() -> S2SRequesterProtocol:
    return S2SRequester()


def get_admin_postback_service(
    uow_factory: UnitOfWorkFactoryProtocol = Depends(get_uow_factory),
    event_bus: IAsyncEventBus = Depends(get_in_memory_event_bus),
    requester: S2SRequesterProtocol = Depends(get_s2s_requester),
    authorization_service: CrmAuthorizationService = Depends(
        get_crm_authorization_service
    ),
) -> PostbackService:
    return PostbackService(uow_factory, event_bus, requester, authorization_service)


def get_app_secrets_encryption_service() -> EncryptionServiceProtocol:
    return EncryptionService()


def get_admin_secrets_service(
    uow_factory: UnitOfWorkFactoryProtocol = Depends(get_uow_factory),
    authorization_service: CrmAuthorizationService = Depends(
        get_crm_authorization_service
    ),
    encryption_service: EncryptionServiceProtocol = Depends(
        get_app_secrets_encryption_service
    ),
) -> SecretsService:
    return SecretsService(uow_factory, authorization_service, encryption_service)


def get_admin_definitions_service(
    uow_factory: UnitOfWorkFactoryProtocol = Depends(get_uow_factory),
    user_service: CrmAuthorizationService = Depends(get_crm_authorization_service),
) -> DefinitionsService:
    return DefinitionsService(uow_factory, user_service)


def get_currency_client() -> CurrencyConvertorClientProtocol:
    return CurrencyConvertorClient()


def get_sdk_ingestion_service(
    uow_factory: UnitOfWorkFactoryProtocol = Depends(get_uow_factory),
    event_bus: IAsyncEventBus = Depends(get_in_memory_event_bus),
    currency_service: CurrencyConvertorClientProtocol = Depends(get_currency_client),
) -> IngestionService:
    return IngestionService(uow_factory, event_bus, currency_service)


def get_hash_service() -> HashProtocol:
    return ServerHash()


def get_sdk_app_service(
    uow_factory: UnitOfWorkFactoryProtocol = Depends(get_uow_factory),
    authorization_service: CrmAuthorizationService = Depends(
        get_crm_authorization_service
    ),
    encryption_service: EncryptionServiceProtocol = Depends(
        get_app_secrets_encryption_service
    ),
    hash_service: HashProtocol = Depends(get_hash_service),
    event_bus: IAsyncEventBus = Depends(get_in_memory_event_bus),
) -> AppService:
    return AppService(
        uow_factory, authorization_service, encryption_service, hash_service, event_bus
    )
