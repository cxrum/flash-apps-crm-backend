from __future__ import annotations

from typing import Mapping, TypeVar

from pydantic import BaseModel

from app.application.tracking.entities import TrackingRedirectCommand

TCommand = TypeVar("TCommand", bound=BaseModel)


class TrackingCommandMapper:
    @staticmethod
    def _to_command(command_type: type[TCommand], payload: Mapping[str, object]) -> TCommand:
        return command_type.model_validate(dict(payload))

    @classmethod
    def redirect_from_transport(cls, payload: Mapping[str, object]) -> TrackingRedirectCommand:
        return cls._to_command(TrackingRedirectCommand, payload)
