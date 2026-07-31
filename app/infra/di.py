from typing import Annotated

from fastapi import Depends

from app.core.bus.contract import IAsyncEventBus
from app.core.bus.di import get_in_memory_event_bus
from app.infra.analytics_attribution_adapter import CrmAnalyticsAttributionAdapter
from app.infra.analytics_logs_adapter import CrmIngestionAnalyticsLogsAdapter
from app.modules.analytics.application.attribution.protocol import AnalyticsAttributionPort
from app.modules.analytics.application.logs.protocol import AnalyticsLogsPort
from app.modules.analytics.di.services import get_analytics_attribution_service, get_analytics_logs_service
from app.modules.crm.application.admin.crm_authorization.protocol import CrmAuthorizationServiceProtocol
from app.modules.crm.application.admin.ingestion.analytics_logs_gateway import AnalyticsLogsGateway
from app.modules.crm.application.admin.ingestion.protocol import IngestionDataServiceProtocol
from app.modules.crm.application.admin.ingestion.service import IngestionDataService
from app.modules.crm.application.admin.postback.protocol import PostbackServiceProtocol
from app.modules.crm.application.admin.postback.service import PostbackService
from app.modules.crm.application.admin.push.protocol import PushServiceProtocol
from app.modules.crm.application.admin.push.service import PushService
from app.modules.crm.application.attribution.protocol import CrmAttributionGateway
from app.modules.crm.application.contracts.requester import S2SRequesterProtocol
from app.modules.crm.di.infra import get_uow_factory
from app.modules.crm.di.services import get_crm_authorization_service, get_s2s_requester
from app.modules.crm.domain.uow import UnitOfWorkFactoryProtocol


def get_crm_ingestion_analytics_logs_adapter(
    analytics_logs: Annotated[AnalyticsLogsPort, Depends(get_analytics_logs_service)],
) -> AnalyticsLogsGateway:
    return CrmIngestionAnalyticsLogsAdapter(analytics_logs)


def get_crm_attribution_gateway(
    analytics_attribution: Annotated[AnalyticsAttributionPort, Depends(get_analytics_attribution_service)],
) -> CrmAttributionGateway:
    return CrmAnalyticsAttributionAdapter(analytics_attribution)


def get_admin_ingestion_data_service(
    analytics_logs_gateway: Annotated[AnalyticsLogsGateway, Depends(get_crm_ingestion_analytics_logs_adapter)],
    uow_factory: Annotated[UnitOfWorkFactoryProtocol, Depends(get_uow_factory)],
    authorization_service: Annotated[CrmAuthorizationServiceProtocol, Depends(get_crm_authorization_service)],
) -> IngestionDataServiceProtocol:
    return IngestionDataService(
        analytics_logs_gateway=analytics_logs_gateway,
        uow_factory=uow_factory,
        authorization_service=authorization_service,
    )


def get_crm_push_service(
    attribution_gateway: Annotated[CrmAttributionGateway, Depends(get_crm_attribution_gateway)],
    uow_factory: Annotated[UnitOfWorkFactoryProtocol, Depends(get_uow_factory)],
    authorization_service: Annotated[CrmAuthorizationServiceProtocol, Depends(get_crm_authorization_service)],
) -> PushServiceProtocol:
    return PushService(uow_factory, authorization_service, attribution_gateway)


def get_crm_postback_service(
    attribution_gateway: Annotated[CrmAttributionGateway, Depends(get_crm_attribution_gateway)],
    uow_factory: Annotated[UnitOfWorkFactoryProtocol, Depends(get_uow_factory)],
    event_bus: Annotated[IAsyncEventBus, Depends(get_in_memory_event_bus)],
    requester: Annotated[S2SRequesterProtocol, Depends(get_s2s_requester)],
    authorization_service: Annotated[CrmAuthorizationServiceProtocol, Depends(get_crm_authorization_service)],
) -> PostbackServiceProtocol:
    return PostbackService(uow_factory, event_bus, requester, attribution_gateway, authorization_service)
