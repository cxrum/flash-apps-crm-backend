from typing import Protocol

from app.modules.analytics.domain.currency.entity import Money


class CurrencyConvertorClientProtocol(Protocol):
    def convert(self, _from: Money, _to: str) -> Money: ...
