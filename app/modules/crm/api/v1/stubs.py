from __future__ import annotations

from typing import Any

from pydantic import BaseModel


def build_stub_response(command: BaseModel) -> str:
    return {
        "status": "stub",
        "command_type": command.__class__.__name__,
        "command": command.model_dump(mode="json", exclude_none=True),
    }.__str__()
