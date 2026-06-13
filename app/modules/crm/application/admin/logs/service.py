from app.modules.crm.application.access_decorators import require_permission
from app.modules.crm.application.admin.crm_authorization.protocol import CrmAuthorizationServiceProtocol
from app.modules.crm.application.admin.logs.commands import (
    ListAuditLogCommand,
    ListClickLogsCommand,
    ListEventLogsCommand,
)
from app.modules.crm.application.admin.logs.mappers import LogsCommandsMapper
from app.modules.crm.application.admin.logs.protocol import LogsServiceProtocol
from app.modules.crm.application.admin.logs.responses import (
    ListAuditLogsResponse,
    ListClickLogsResponse,
    ListRawEventsResponse,
)
from app.modules.crm.application.mapper import PaginationMapper
from app.modules.crm.domain.permission.CrmPermissionEntity import CrmPermissionEntity
from app.modules.crm.domain.uow import UnitOfWorkFactoryProtocol


class LogsService(LogsServiceProtocol):
    def __init__(
        self,
        uow_factory: UnitOfWorkFactoryProtocol,
        authorization_service: CrmAuthorizationServiceProtocol,
    ) -> None:
        self._uow_factory = uow_factory
        self._authorization_service = authorization_service

    @require_permission(CrmPermissionEntity.view_raw_logs_permission())
    def list_clicks(
        self,
        command: ListClickLogsCommand,
    ) -> ListClickLogsResponse:
        with self._uow_factory.create() as uow:
            clicks = uow.click_repo.list_by_app_id(
                command.app_id,
                click_id=command.click_id,
                pagination=PaginationMapper.pagination_from_command(command),
            )

        return ListClickLogsResponse(clicks=[LogsCommandsMapper.click_log_domain_to_value(it) for it in clicks])

    @require_permission(CrmPermissionEntity.view_raw_logs_permission())
    def list_raw_events(
        self,
        command: ListEventLogsCommand,
    ) -> ListRawEventsResponse:
        with self._uow_factory.create() as uow:
            events = uow.event_repo.list_by_app_id(
                command.app_id,
                click_id=command.click_id,
                event_key=command.event_key,
                pagination=PaginationMapper.pagination_from_command(command),
            )

        return ListRawEventsResponse(events=[LogsCommandsMapper.event_log_domain_to_value(it) for it in events])

    def list_audit_logs(
        self,
        command: ListAuditLogCommand,
    ) -> ListAuditLogsResponse:
        if command.app_id is not None:
            self._authorization_service.has_user_app_access(
                crm_user_id=command.crm_user_id,
                app_id=command.app_id,
            )

        with self._uow_factory.create() as uow:
            if command.app_id is not None:
                audit_logs = uow.audit_log_repo.list_by_app_id(
                    command.app_id,
                    actor_id=command.actor_id,
                    entity_type=command.entity_type,
                    entity_id=command.entity_id,
                    pagination=PaginationMapper.pagination_from_command(command),
                )
            elif command.actor_id is not None:
                audit_logs = uow.audit_log_repo.list_by_user_id(
                    command.actor_id,
                    entity_type=command.entity_type,
                    entity_id=command.entity_id,
                    pagination=PaginationMapper.pagination_from_command(command),
                )
            else:
                audit_logs = []

        return ListAuditLogsResponse(audit_logs=[LogsCommandsMapper.audit_log_domain_to_value(it) for it in audit_logs])
