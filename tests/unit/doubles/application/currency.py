from __future__ import annotations

from copy import copy

from app.domain.currency.currency_convertor_protocol import CurrencyConvertorClientProtocol
from app.domain.currency.entity import Money
from tests.unit.doubles.base import CallRecorderMixin


class StubCurrencyConvertorClient(CallRecorderMixin, CurrencyConvertorClientProtocol):
    def __init__(self) -> None:
        super().__init__()
        self.rates: dict[tuple[str, str], float] = {
            ("EUR", "USD"): 1.2,
            ("USD", "EUR"): 0.8,
        }

    def seed_rate(self, *, source: str, target: str, rate: float) -> None:
        self.rates[(source.upper(), target.upper())] = rate

    def convert(self, _from: Money, _to: str) -> Money:
        self._record("convert", _from, _to)
        target = _to.upper()
        source = _from.base.upper()

        if source == target:
            return copy(_from)

        rate = self.rates[(source, target)]
        return Money(base=target, value=_from.value * rate)
