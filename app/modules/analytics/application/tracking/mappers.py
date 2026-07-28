from __future__ import annotations

from collections.abc import Mapping

from app.modules.analytics.application.tracking.entities import TrackingRedirectCommand
from app.modules.crm.core.utils.general_mapper import GeneralMapper


class TrackingCommandMapper:
    @classmethod
    def redirect_from_transport(cls, payload: Mapping[str, object]) -> TrackingRedirectCommand:
        return GeneralMapper.command_payload_to_command(TrackingRedirectCommand, payload)
