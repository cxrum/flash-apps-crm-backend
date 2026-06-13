from __future__ import annotations

from typing import Mapping, TypeVar

from pydantic import BaseModel

from app.modules.crm.application.tracking.entities import TrackingRedirectCommand
from app.modules.crm.core.utils.general_mapper import GeneralMapper

TCommand = TypeVar("TCommand", bound=BaseModel)


class TrackingCommandMapper:
    @classmethod
    def redirect_from_transport(cls, payload: Mapping[str, object]) -> TrackingRedirectCommand:
        return GeneralMapper.command_payload_to_command(TrackingRedirectCommand, payload)
