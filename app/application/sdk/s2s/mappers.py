from __future__ import annotations

from typing import Mapping, TypeVar

from pydantic import BaseModel

from app.application.sdk.s2s.commands import S2SClickCommand
from app.core.utils.general_mapper import GeneralMapper

TCommand = TypeVar("TCommand", bound=BaseModel)


class S2SCommandMapper:
    @classmethod
    def click_from_transport(cls, payload: Mapping[str, object]) -> S2SClickCommand:
        return  GeneralMapper.command_payload_to_command(S2SClickCommand, payload)
