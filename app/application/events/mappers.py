from __future__ import annotations

from app.application.events.entities import EventsBatchCommand, IngestEventsBatchCommand


class IngestEventsBatchCommandMapper:
    @staticmethod
    def from_transport(
        *,
        app_id: int,
        env: str,
        signature: str,
        payload: EventsBatchCommand,
    ) -> IngestEventsBatchCommand:
        return IngestEventsBatchCommand(
            app_id=app_id,
            env=env,
            signature=signature,
            payload=payload,
        )

