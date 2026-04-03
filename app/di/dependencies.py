import logging
from collections.abc import AsyncIterator, Awaitable, Callable, Sequence
from contextlib import asynccontextmanager
from functools import lru_cache
from typing import Any

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

from app.application.admin.push.service import PushService
from app.application.contracts.ip2location import IP2LocationGatewayProtocol
from app.application.crm_authentication.protocol import CrmAuthenticationProtocol
from app.application.crm_authentication.responses import ResolvedCrmUserResponse
from app.application.crm_authentication.service import CrmAuthentication
from app.application.admin.crm_authorization.service import CrmAuthorizationService
from app.application.admin.definitions.service import DefinitionsService
from app.application.admin.logs.service import LogsService
from app.application.admin.postback.service import PostbackService
from app.application.admin.secrets.service import SecretsService
from app.application.contracts.encryption import EncryptionServiceProtocol
from app.application.contracts.requester import S2SRequesterProtocol
from app.application.exception_bus.handlers.stub import AsyncStubExceptionHandler
from app.application.events_bus.handlers.conversion import AsyncConversionHandler
from app.application.events_bus.handlers.metric import AsyncMetricHandler
from app.application.events_bus.handlers.update_param import AsyncUpdateParamHandler
from app.application.exceptions import ApplicationError
from app.application.sdk.apps.service import AppService
from app.application.sdk.ingestion.service import IngestionService
from app.application.sdk.s2s.service import ClickService
from app.core.config import settings
from app.domain.currency.currency_convertor_protocol import CurrencyConvertorClientProtocol
from app.domain.event_bus.events.crm_events import ConversionEventMessage, MetricEventMessage
from app.domain.event_bus.events.exception_event import ExceptionEvent
from app.domain.event_bus.events.crm_update_params import UpdateCurrentParamMessage
from app.domain.event_bus.service_protocol import (
    AsyncEventMessageHandler,
    IAsyncEventBus,
    IAsyncExceptionBus,
)
from app.domain.hash_protocol import HashProtocol
from app.domain.signature_protocol import SignatureProtocol
from app.domain.uow import UnitOfWorkFactoryProtocol
from app.infra.db.puow import SqlAlchemyUnitOfWorkFactory
from app.infra.db.session import SessionFactory
from app.infra.event_bus.async_bus.in_memory import InMemoryAsyncEventBus
from app.infra.exception_bus.exception_bus import AsyncExceptionBusAdapter
from app.infra.services.currency import CurrencyConvertorClient
from app.infra.services.encryption import EncryptionService
from app.infra.services.hashing import ServerHash
from app.infra.services.ip2location import IP2LocationGateway
from app.infra.services.s2s.request_builder import S2SRequester
from app.infra.services.signature import SignatureSHA256


AsyncHandlerSubscription = tuple[str, AsyncEventMessageHandler]
FastAPIExceptionHandler = Callable[[Request, Any], Awaitable[JSONResponse]]

SHARED_ASYNC_MEMORY_BUS = InMemoryAsyncEventBus()
SHARED_ASYNC_MEMORY_EXCEPTION_BUS = AsyncExceptionBusAdapter(InMemoryAsyncEventBus())
logger = logging.getLogger(__name__)


def get_uow_factory() -> UnitOfWorkFactoryProtocol:
    return SqlAlchemyUnitOfWorkFactory(SessionFactory)

def get_ip2location_gateway() ->IP2LocationGatewayProtocol:
    return  IP2LocationGateway(settings.ip2location_bin_database_path)

def get_app_secrets_encryption_service() -> EncryptionServiceProtocol:
    return EncryptionService()

def get_hash_service() -> HashProtocol:
    return ServerHash()

def get_signature_sha256_service() -> SignatureProtocol:
    return SignatureSHA256()

def get_currency_client() -> CurrencyConvertorClientProtocol:
    return CurrencyConvertorClient()


def get_in_memory_event_bus() -> IAsyncEventBus:
    return SHARED_ASYNC_MEMORY_BUS


def get_in_memory_exception_event_bus() -> IAsyncExceptionBus:
    return SHARED_ASYNC_MEMORY_EXCEPTION_BUS


def build_update_param_handler(
    uow_factory: UnitOfWorkFactoryProtocol,
) -> AsyncEventMessageHandler:
    return AsyncUpdateParamHandler(uow_factory)


def build_metric_handler(
    uow_factory: UnitOfWorkFactoryProtocol,
) -> AsyncEventMessageHandler:
    return AsyncMetricHandler(uow_factory)


def build_conversion_handler(
    uow_factory: UnitOfWorkFactoryProtocol,
) -> AsyncEventMessageHandler:
    return AsyncConversionHandler(uow_factory)


def build_stub_exception_handler() -> AsyncEventMessageHandler:
    return AsyncStubExceptionHandler()


@lru_cache
def get_exception_event_subscribers() -> tuple[AsyncHandlerSubscription, ...]:
    return (
        (ExceptionEvent.EVENT_NAME, build_stub_exception_handler()),
    )


def register_exception_event_handlers(
    async_handlers: Sequence[AsyncHandlerSubscription] | None = None,
    async_memory_bus: IAsyncExceptionBus | None = None,
) -> IAsyncExceptionBus:
    handlers = (
        get_exception_event_subscribers()
        if async_handlers is None
        else tuple(async_handlers)
    )
    exception_bus = (
        get_in_memory_exception_event_bus()
        if async_memory_bus is None
        else async_memory_bus
    )

    for event_name, handler in handlers:
        exception_bus.subscribe(event_name, handler)

    return exception_bus


@lru_cache
def get_event_subscribers() -> tuple[AsyncHandlerSubscription, ...]:
    uow_factory = get_uow_factory()

    return (
        (
            UpdateCurrentParamMessage.EVENT_NAME,
            build_update_param_handler(uow_factory),
        ),
        (
            MetricEventMessage.EVENT_NAME,
            build_metric_handler(uow_factory),
        ),
        (
            ConversionEventMessage.EVENT_NAME,
            build_conversion_handler(uow_factory),
        ),
    )


def register_event_handlers(
    async_handlers: Sequence[AsyncHandlerSubscription] | None = None,
    async_memory_bus: IAsyncEventBus | None = None,
) -> IAsyncEventBus:
    handlers = (
        get_event_subscribers()
        if async_handlers is None
        else tuple(async_handlers)
    )
    event_bus = (
        get_in_memory_event_bus()
        if async_memory_bus is None
        else async_memory_bus
    )

    for event_name, handler in handlers:
        event_bus.subscribe(event_name, handler)

    return event_bus


def wire_application_buses(
    event_bus: IAsyncEventBus | None = None,
    exception_bus: IAsyncExceptionBus | None = None,
) -> tuple[IAsyncEventBus, IAsyncExceptionBus]:
    wired_exception_bus = register_exception_event_handlers(
        async_memory_bus=exception_bus,
    )
    wired_event_bus = register_event_handlers(
        async_memory_bus=event_bus,
    )
    return wired_event_bus, wired_exception_bus


def build_fastapi_exception_handler(
    exception_bus: IAsyncExceptionBus | None = None,
) -> FastAPIExceptionHandler:
    bus = (
        get_in_memory_exception_event_bus()
        if exception_bus is None
        else exception_bus
    )

    async def handler(request: Request, exc: Exception) -> JSONResponse:
        event = ExceptionEvent(
            name=ExceptionEvent.EVENT_NAME,
            payload={
                "exception_type": type(exc).__name__,
                "exception_message": str(exc),
                "context": {
                    "method": request.method,
                    "path": request.url.path,
                    "query_params": dict(request.query_params),
                    "client_host": None if request.client is None else request.client.host,
                },
            },
        )

        try:
            await bus.publish(event)
        except Exception:
            logger.exception(
                "Failed to publish exception event",
                extra={
                    "path": request.url.path,
                    "exception_type": type(exc).__name__,
                },
            )

        if settings.debug_mode:
            return JSONResponse(
                status_code=500,
                content=event.payload,
            )
        else:
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal Server Error"},
            )

    return handler


def register_fastapi_exception_handlers(
    app: FastAPI,
    exception_bus: IAsyncExceptionBus | None = None,
) -> FastAPI:
    app.add_exception_handler(ApplicationError, build_fastapi_exception_handler(exception_bus))
    return app


@asynccontextmanager
async def application_lifespan(app: FastAPI) -> AsyncIterator[None]:
    event_bus, exception_bus = wire_application_buses(
        event_bus=get_in_memory_event_bus(),
        exception_bus=get_in_memory_exception_event_bus(),
    )

    await exception_bus.start()
    await event_bus.start()
    try:
        yield
    finally:
        await event_bus.stop()
        await exception_bus.stop()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@lru_cache
def stub_user_resolver(
    uow_factory: UnitOfWorkFactoryProtocol = Depends(get_uow_factory),
    hash_service: HashProtocol = Depends(get_hash_service)
) -> CrmAuthenticationProtocol:
    return CrmAuthentication(
        uow_factory,
        hash_service
    )

def verify_token(token: str = Depends(oauth2_scheme), user_resolver: CrmAuthenticationProtocol = Depends(stub_user_resolver)) -> str:
    return user_resolver.verify_token(token)

def resolve_user(token: str = Depends(oauth2_scheme), user_resolver: CrmAuthenticationProtocol = Depends(stub_user_resolver)) -> ResolvedCrmUserResponse:
    return user_resolver.resolve_user(token)

def get_sdk_app_service(
    uow_factory: UnitOfWorkFactoryProtocol = Depends(get_uow_factory),
    encryption_service: EncryptionServiceProtocol = Depends(get_app_secrets_encryption_service),
    hash_service: HashProtocol = Depends(get_hash_service)
) -> AppService:
    return AppService(uow_factory, encryption_service, hash_service)


def get_sdk_ingestion_service(
    uow_factory: UnitOfWorkFactoryProtocol = Depends(get_uow_factory),
    event_bus: IAsyncEventBus = Depends(get_in_memory_event_bus),
    currency_service: CurrencyConvertorClientProtocol = Depends(get_currency_client),
) -> IngestionService:
    return IngestionService(uow_factory, event_bus, currency_service)


def get_s2s_requester() -> S2SRequesterProtocol:
    return S2SRequester()


def get_crm_authorization_service(
    uow_factory: UnitOfWorkFactoryProtocol = Depends(get_uow_factory),
) -> CrmAuthorizationService:
    return CrmAuthorizationService(uow_factory)


def get_admin_definitions_service(
    uow_factory: UnitOfWorkFactoryProtocol = Depends(get_uow_factory),
    user_service: CrmAuthorizationService = Depends(get_crm_authorization_service),
) -> DefinitionsService:
    return DefinitionsService(uow_factory, user_service)


def get_admin_secrets_service(
    uow_factory: UnitOfWorkFactoryProtocol = Depends(get_uow_factory),
    authorization_service: CrmAuthorizationService = Depends(get_crm_authorization_service),
    encryption_service: EncryptionServiceProtocol = Depends(get_app_secrets_encryption_service),
) -> SecretsService:
    return SecretsService(uow_factory, authorization_service, encryption_service)


def get_admin_postback_service(
    uow_factory: UnitOfWorkFactoryProtocol = Depends(get_uow_factory),
    event_bus: IAsyncEventBus = Depends(get_in_memory_event_bus),
    requester: S2SRequesterProtocol = Depends(get_s2s_requester),
    authorization_service: CrmAuthorizationService = Depends(get_crm_authorization_service),
) -> PostbackService:
    return PostbackService(uow_factory, event_bus, requester, authorization_service)


def get_admin_logs_service(
    uow_factory: UnitOfWorkFactoryProtocol = Depends(get_uow_factory),
    authorization_service: CrmAuthorizationService = Depends(get_crm_authorization_service),
) -> LogsService:
    return LogsService(
        uow_factory,
        authorization_service
    )

def get_push_service(
    uow_factory: UnitOfWorkFactoryProtocol = Depends(get_uow_factory),
    authorization_service: CrmAuthorizationService = Depends(get_crm_authorization_service),
) -> PushService:
    return PushService(
        uow_factory=uow_factory,
        authorization_service=authorization_service
    )

def get_s2s_service(
    uow_factory: UnitOfWorkFactoryProtocol = Depends(get_uow_factory),
    signature_service: SignatureProtocol = Depends(get_signature_sha256_service),
    ip2location_gateway: IP2LocationGatewayProtocol = Depends(get_ip2location_gateway)
) -> ClickService:
    return ClickService(
        uow_factory,
        signature_service,
        ip2location_gateway
    )
