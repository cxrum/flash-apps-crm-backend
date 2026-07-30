from typing import Annotated

from fastapi import Depends

from app.core.bus.contract import IAsyncEventBus
from app.modules.analytics.application.ingestion.protocol import IngestionServiceProtocol
from app.modules.analytics.application.ingestion.service import IngestionService
from app.modules.analytics.application.logs.protocol import AnalyticsLogsPort
from app.modules.analytics.application.logs.service import AnalyticsLogsService
from app.modules.analytics.application.s2s.protocol import ClickServiceProtocol
from app.modules.analytics.application.s2s.service import ClickService
from app.modules.analytics.di.event_bus import get_analytics_event_bus
from app.modules.analytics.di.infra import get_analytics_uow_factory, get_idempotency_repository
from app.modules.analytics.domain.redis.repo import IdempotencyKeyRepositoryProtocol
from app.modules.analytics.domain.signature_protocol import AnalyticsSignatureProtocol
from app.modules.analytics.domain.uow import AnalyticsUnitOfWorkFactoryProtocol
from app.modules.analytics.infra.services.signature import AnalyticsSignatureSHA256
from app.modules.crm.application.contracts.ip2location import IP2LocationGatewayProtocol
from app.modules.crm.di.services import get_currency_client, get_ip2location_gateway
from app.modules.crm.domain.currency.currency_convertor_protocol import CurrencyConvertorClientProtocol


def get_analytics_signature_sha256_service() -> AnalyticsSignatureProtocol:
    return AnalyticsSignatureSHA256()


def get_analytics_click_service(
    uow_factory: Annotated[AnalyticsUnitOfWorkFactoryProtocol, Depends(get_analytics_uow_factory)],
    signature_service: Annotated[AnalyticsSignatureProtocol, Depends(get_analytics_signature_sha256_service)],
    ip2location_gateway: Annotated[IP2LocationGatewayProtocol, Depends(get_ip2location_gateway)],
) -> ClickServiceProtocol:
    return ClickService(uow_factory, signature_service, ip2location_gateway)


def get_analytics_ingestion_service(
    uow_factory: Annotated[AnalyticsUnitOfWorkFactoryProtocol, Depends(get_analytics_uow_factory)],
    event_bus: Annotated[IAsyncEventBus, Depends(get_analytics_event_bus)],
    currency_service: Annotated[CurrencyConvertorClientProtocol, Depends(get_currency_client)],
    idempotency_repo: Annotated[IdempotencyKeyRepositoryProtocol, Depends(get_idempotency_repository)],
) -> IngestionServiceProtocol:
    return IngestionService(uow_factory, event_bus, currency_service, idempotency_repo)


def get_analytics_logs_service(
    uow_factory: Annotated[AnalyticsUnitOfWorkFactoryProtocol, Depends(get_analytics_uow_factory)],
) -> AnalyticsLogsPort:
    return AnalyticsLogsService(uow_factory)
