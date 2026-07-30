from app.modules.crm.application.admin.audit.commands import (
    ListAuditLogCommand,
)
from app.modules.crm.application.admin.audit.mappers import AuditCommandsMapper
from app.modules.crm.application.admin.audit.protocol import AuditServiceProtocol
from app.modules.crm.application.admin.audit.responses import (
    ListAuditLogsResponse,
)
from app.modules.crm.application.admin.crm_authorization.protocol import CrmAuthorizationServiceProtocol
from app.modules.crm.application.mapper import PaginationMapper
from app.modules.crm.domain.uow import UnitOfWorkFactoryProtocol


class AuditService(AuditServiceProtocol):
    def __init__(
        self,
        uow_factory: UnitOfWorkFactoryProtocol,
        authorization_service: CrmAuthorizationServiceProtocol,
    ) -> None:
        self._uow_factory = uow_factory
        self._authorization_service = authorization_service

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

        return ListAuditLogsResponse(
            audit_logs=[AuditCommandsMapper.audit_log_domain_to_value(it) for it in audit_logs]
        )
