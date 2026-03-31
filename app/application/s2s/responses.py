

from dataclasses import dataclass


@dataclass(frozen=True)
class S2SClickResponse:
    click_id: str

