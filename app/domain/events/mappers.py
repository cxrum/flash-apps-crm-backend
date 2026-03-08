from __future__ import annotations

from datetime import datetime

from app.application.events.entities import EventItemCommand
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
    
    @staticmethod
    def from_payload(
        event_data: EventItemCommand ,
        *,
        app_id: int,
        environment: str,
        sdk_version: str,
        sent_at: datetime,
    ) -> EventEntity:
        return EventEntity(
            event_id=event_data.event_id,
            app_id=app_id,
            event_name=event_data.event_name,
            event_time=event_data.event_time,
            platform=event_data.platform,
            anonymous_id=event_data.ids.anonymous_id,
            user_id=event_data.ids.user_id,
            source=event_data.attribution.source,
            campaign=event_data.attribution.campaign,
            medium=event_data.attribution.adset,
            params={
                "sdk_version": sdk_version,
                "sent_at": sent_at.isoformat(),
                "app_version": event_data.app_version,
                "device": event_data.device,
                "attribution": event_data.attribution,
                "geo": event_data.geo,
                "env": environment,
                "payload": event_data.params,
            },
        )
