from __future__ import annotations

from typing import Mapping, TypeVar

from pydantic import BaseModel

from app.application.s2s.commands import S2SClickCommand

TCommand = TypeVar("TCommand", bound=BaseModel)


class S2SCommandMapper:
    @staticmethod
    def _to_command(command_type: type[TCommand], payload: Mapping[str, object]) -> TCommand:
        return command_type.model_validate(dict(payload))

    @classmethod
    def click_from_transport(cls, payload: Mapping[str, object]) -> S2SClickCommand:
        return cls._to_command(S2SClickCommand, payload)
