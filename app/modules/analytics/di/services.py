from fastapi import Depends

from app.core.bus.contract import IAsyncEventBus
from app.modules.analytics.application.admin.logs.protocol import AnalyticsLogsServiceProtocol
from app.modules.analytics.application.admin.logs.service import AnalyticsLogsService
from app.modules.analytics.application.ingestion.protocol import IngestionServiceProtocol
from app.modules.analytics.application.ingestion.service import IngestionService
from app.modules.analytics.application.s2s.protocol import ClickServiceProtocol
from app.modules.analytics.application.s2s.service import ClickService
from app.modules.analytics.di.event_bus import get_analytics_event_bus
from app.modules.analytics.di.infra import get_analytics_uow_factory, get_idempotency_repository
from app.modules.analytics.domain.redis.repo import IdempotencyKeyRepositoryProtocol
from app.modules.analytics.domain.uow import AnalyticsUnitOfWorkFactoryProtocol
from app.modules.crm.application.contracts.ip2location import IP2LocationGatewayProtocol
from app.modules.crm.di.services import get_currency_client, get_ip2location_gateway, get_signature_sha256_service
from app.modules.crm.domain.currency.currency_convertor_protocol import CurrencyConvertorClientProtocol
from app.modules.crm.domain.signature_protocol import SignatureProtocol


def get_analytics_click_service(
    uow_factory: AnalyticsUnitOfWorkFactoryProtocol = Depends(get_analytics_uow_factory),
    signature_service: SignatureProtocol = Depends(get_signature_sha256_service),
    ip2location_gateway: IP2LocationGatewayProtocol = Depends(get_ip2location_gateway),
) -> ClickServiceProtocol:
    return ClickService(uow_factory, signature_service, ip2location_gateway)


def get_analytics_ingestion_service(
    uow_factory: AnalyticsUnitOfWorkFactoryProtocol = Depends(get_analytics_uow_factory),
    event_bus: IAsyncEventBus = Depends(get_analytics_event_bus),
    currency_service: CurrencyConvertorClientProtocol = Depends(get_currency_client),
    idempotency_repo: IdempotencyKeyRepositoryProtocol = Depends(get_idempotency_repository),
) -> IngestionServiceProtocol:
    return IngestionService(uow_factory, event_bus, currency_service, idempotency_repo)


def get_analytics_logs_service(
    uow_factory: AnalyticsUnitOfWorkFactoryProtocol = Depends(get_analytics_uow_factory),
) -> AnalyticsLogsServiceProtocol:
    return AnalyticsLogsService(uow_factory)
