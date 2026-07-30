from copy import copy

import requests

from app.modules.analytics.domain.currency.currency_convertor_protocol import CurrencyConvertorClientProtocol
from app.modules.analytics.domain.currency.entity import Money


class CurrencyConvertorClient(CurrencyConvertorClientProtocol):
    def __init__(self) -> None:
        self.base_url = "https://api.frankfurter.dev/v1/latest"

    def convert(self, _from: Money, _to: str) -> Money:
        if _from.base == _to:
            return copy(_from)
        if len(_to) != 3 or len(_from.base) != 3:
            raise RuntimeError("Inncorect base code")

        response = requests.get(self.base_url, params={"base": _from.base, "symbols": _to})
        if response.status_code != 200:
            raise RuntimeError("Currency service error")
        return Money(base=_to, value=_from.value * float(response.json()["rates"][_to]))
