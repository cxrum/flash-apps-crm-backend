from app.application.events_bus.events import RawEventMessage
from app.application.exceptions import ApplicationError
from app.domain.events.CrmEventEntity import EventEntity


from collections.abc import Mapping, Sequence
from typing import Any, TypeVar

TRawEventMessage = TypeVar("TRawEventMessage", bound=RawEventMessage)

class RawEventMessageFactory:
    DEFAULT_SOURCE = "sdk"

    @classmethod
    def from_event(
        cls,
        event: EventEntity,
        *,
        metadata: Mapping[str, Any] | None = None,
        name: str = RawEventMessage.EVENT_NAME,
        message_cls: type[TRawEventMessage] = RawEventMessage,
    ) -> TRawEventMessage:
        if not event.event_id:
            raise ApplicationError("Event id is required for RawEventMessage")
        if not event.click_id:
            raise ApplicationError("Click id is required for RawEventMessage")

        message_metadata = {
            "source": cls.DEFAULT_SOURCE,
            **dict(metadata or {}),
        }
        return message_cls(
            name=name,
            payload={
                "event_id": event.event_id,
                "click_id": event.click_id,
                "event_type": event.event_type,
                "event_key": event.event_key,
                "app_user_id": event.app_user_id,
                "amount": event.amount,
                "currency": event.currency,
                "amount_usd": event.amount_usd,
                "event_time_utc": event.event_time_utc,
                "payload": dict(event.payload),
                "created_at": event.created_at,
            },
            metadata=message_metadata,
            occurred_at=event.created_at or event.event_time_utc,
        )

    @classmethod
    def from_events(
        cls,
        events: Sequence[EventEntity],
        *,
        metadata: Mapping[str, Any] | None = None,
        name: str = RawEventMessage.EVENT_NAME,
        message_cls: type[TRawEventMessage] = RawEventMessage,
    ) -> list[TRawEventMessage]:
        return [
            cls.from_event(
                event,
                metadata=metadata,
                name=name,
                message_cls=message_cls,
            )
            for event in events
        ]