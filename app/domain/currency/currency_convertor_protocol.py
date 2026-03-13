
from typing import Protocol

from app.domain.currency.entity import CurrencyEntity


class CurrencyConvertorClientProtocol(Protocol):
    def convert(self, _from: CurrencyEntity, _to: str) -> CurrencyEntity: ...
