
from dataclasses import dataclass


@dataclass
class CurrencyEntity:
    base: str
    value: float