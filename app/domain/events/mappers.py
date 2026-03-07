from __future__ import annotations

from datetime import datetime

from app.contracts.events import EventRecordDTO
from app.domain.events.entities import EventEntity


class EventEntityMapper:
    @staticmethod
    def from_dict(
        event_data: dict,
        *,
        app_id: int,
        environment: str,
        sdk_version: str,
        sent_at: datetime,
    ) -> EventEntity:
        return EventEntity(
            event_id=event_data["event_id"],
            app_id=app_id,
            event_name=event_data["event_name"],
            event_time=event_data["event_time"],
            platform=event_data["platform"],
            anonymous_id=event_data["ids"]["anonymous_id"],
            user_id=event_data["ids"]["user_id"],
            source=event_data["attribution"]["source"],
            campaign=event_data["attribution"]["campaign"],
            medium=event_data["attribution"]["adset"],
            params={
                "sdk_version": sdk_version,
                "sent_at": sent_at.isoformat(),
                "app_version": event_data["app_version"],
                "device": event_data["device"],
                "attribution": event_data["attribution"],
                "geo": event_data["geo"],
                "env": environment,
                "payload": event_data["params"],
            },
        )


class EventPersistenceMapper:
    @staticmethod
    def to_dto(event: EventEntity) -> EventRecordDTO:
        return EventRecordDTO(
            event_id=event.event_id,
            app_id=event.app_id,
            event_name=event.event_name,
            event_time=event.event_time,
            platform=event.platform,
            anonymous_id=event.anonymous_id,
            user_id=event.user_id,
            source=event.source,
            campaign=event.campaign,
            medium=event.medium,
            params=event.params,
        )
