from dataclasses import dataclass


@dataclass(frozen=True)
class Money:
    base: str
    value: float
    rate_to_USD: float | None = None
