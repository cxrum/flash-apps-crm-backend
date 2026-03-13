from app.application.events_bus.events import ConversionEventMessage, DomainEventMessage, MetricEventMessage, RawEventMessage
from app.application.events_bus.factories.raw_event import RawEventMessageFactory
from app.domain.events.CrmEventEntity import EventEntity

from collections.abc import Mapping, Sequence
from typing import Any, Protocol

class EventMessageFactoryStrategyProtocol(Protocol):
    def supports(self, event: EventEntity) -> bool: ...

    def create(
        self,
        event: EventEntity,
        *,
        metadata: Mapping[str, Any] | None = None,
    ) -> DomainEventMessage: ...


class _TypedEventMessageFactoryStrategy:
    def __init__(
        self,
        *,
        event_type: str,
        message_cls: type[RawEventMessage],
    ) -> None:
        self._event_type = event_type
        self._message_cls = message_cls

    def supports(self, event: EventEntity) -> bool:
        return event.event_type == self._event_type

    def create(
        self,
        event: EventEntity,
        *,
        metadata: Mapping[str, Any] | None = None,
    ) -> RawEventMessage:
        return RawEventMessageFactory.from_event(
            event,
            metadata=metadata,
            name=self._message_cls.EVENT_NAME,
            message_cls=self._message_cls,
        )


class _RawEventMessageFactoryStrategy:
    def supports(self, event: EventEntity) -> bool:
        return True

    def create(
        self,
        event: EventEntity,
        *,
        metadata: Mapping[str, Any] | None = None,
    ) -> RawEventMessage:
        return RawEventMessageFactory.from_event(event, metadata=metadata)


class SdkEventMessageFactory:
    _strategies: tuple[EventMessageFactoryStrategyProtocol, ...] = (
        _TypedEventMessageFactoryStrategy(
            event_type="metric",
            message_cls=MetricEventMessage,
        ),
        _TypedEventMessageFactoryStrategy(
            event_type="conversion",
            message_cls=ConversionEventMessage,
        ),
    )
    _fallback_strategy: EventMessageFactoryStrategyProtocol = (
        _RawEventMessageFactoryStrategy()
    )

    @classmethod
    def from_event(
        cls,
        event: EventEntity,
        *,
        metadata: Mapping[str, Any] | None = None,
    ) -> DomainEventMessage:
        strategy = cls._resolve_strategy(event)
        return strategy.create(event, metadata=metadata)

    @classmethod
    def from_events(
        cls,
        events: Sequence[EventEntity],
        *,
        metadata: Mapping[str, Any] | None = None,
    ) -> list[DomainEventMessage]:
        return [
            cls.from_event(event, metadata=metadata)
            for event in events
        ]

    @classmethod
    def _resolve_strategy(
        cls,
        event: EventEntity,
    ) -> EventMessageFactoryStrategyProtocol:
        for strategy in cls._strategies:
            if strategy.supports(event):
                return strategy
        return cls._fallback_strategy