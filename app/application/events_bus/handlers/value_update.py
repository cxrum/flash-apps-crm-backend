from app.application.exception import GeneralException
from app.domain.audit_log.CrmAuditLogEntity import CrmAuditLogEntity
from app.domain.event_bus.entity import DomainEventMessage
from app.domain.event_bus.events.crm_value_update_event import ValueChangedEvent
from app.domain.event_bus.service_protocol import AsyncEventMessageHandler
from app.domain.uow import UnitOfWorkFactoryProtocol


class AsyncAuditValueHandler(AsyncEventMessageHandler):
    def __init__(self, uow_factory: UnitOfWorkFactoryProtocol) -> None:
        self.__uow_factory = uow_factory

    async def handle(self, message: DomainEventMessage) -> None:
        if not isinstance(message, ValueChangedEvent):
            raise GeneralException(
                f"AsyncAuditValueHandler expected ValueChangedEvent, got {type(message).__name__}"
            )

        audit_log = CrmAuditLogEntity.create_from_diff(
            message.old_value,
            message.new_value,
            user_id=message.crm_user_id,
            app_id=message.app_id,
            entity_id=message.entity_id,
            changed_at=message.updated_at,
            ignore_fields=message.ignore_fields,
        )

        with self.__uow_factory.create() as uow:
            uow.audit_log_repo.insert_many(audit_log)

        return None
