from __future__ import annotations

from copy import deepcopy
from typing import Any


class EventPayloadFactory:
    @staticmethod
    def build() -> dict[str, Any]:
        return deepcopy(
            {
                "event_id": "evt-uuid-1",
                "event_name": "first_open",
                "event_time": "2026-03-05T11:59:00Z",
                "platform": "ios",
                "app_version": "1.0.3",
                "device": {
                    "os_version": "17.3",
                    "model": "iPhone16,2",
                    "language": "uk",
                    "timezone": "Europe/Kyiv",
                },
                "ids": {
                    "anonymous_id": "anon-uuid-1",
                    "user_id": "user-1",
                },
                "attribution": {
                    "click_id": None,
                    "source": "organic",
                    "campaign": None,
                    "adset": None,
                    "ad": None,
                },
                "geo": {
                    "country": "UA",
                    "ip": None,
                },
                "params": {"screen": "onboarding"},
            }
        )


class EventsPayloadFactory:
    @staticmethod
    def build() -> dict[str, Any]:
        return deepcopy(
            {
                "sdk_version": "1.0.0",
                "sent_at": "2026-03-05T12:00:00Z",
                "events": [EventPayloadFactory.build()],
            }
        )
