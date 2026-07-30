from typing import Annotated

from fastapi import Depends

from app.infra.analytics_logs_adapter import CrmIngestionAnalyticsLogsAdapter
from app.modules.analytics.application.logs.protocol import AnalyticsLogsPort
from app.modules.analytics.di.services import get_analytics_logs_service
from app.modules.crm.application.admin.crm_authorization.protocol import CrmAuthorizationServiceProtocol
from app.modules.crm.application.admin.ingestion.analytics_logs_gateway import AnalyticsLogsGateway
from app.modules.crm.application.admin.ingestion.protocol import IngestionDataServiceProtocol
from app.modules.crm.application.admin.ingestion.service import IngestionDataService
from app.modules.crm.di.infra import get_uow_factory
from app.modules.crm.di.services import get_crm_authorization_service
from app.modules.crm.domain.uow import UnitOfWorkFactoryProtocol


def get_crm_ingestion_analytics_logs_adapter(
    analytics_logs: Annotated[AnalyticsLogsPort, Depends(get_analytics_logs_service)],
) -> AnalyticsLogsGateway:
    return CrmIngestionAnalyticsLogsAdapter(analytics_logs)


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
