from __future__ import annotations

import pytest

from app.modules.crm.domain.currency.entity import Money
from app.modules.crm.infra.services.currency import CurrencyConvertorClient


class _FakeResponse:
    def __init__(self, *, status_code: int, payload: dict[str, object]) -> None:
        self.status_code = status_code
        self._payload = payload

    def json(self) -> dict[str, object]:
        return self._payload


def test_convert_returns_copy_when_currency_is_already_target_currency() -> None:
    service = CurrencyConvertorClient()
    money = Money(base="USD", value=4.4)

    converted = service.convert(money, "USD")

    assert converted == money
    assert converted is not money


def test_convert_raises_for_invalid_currency_code() -> None:
    service = CurrencyConvertorClient()

    with pytest.raises(RuntimeError, match="Inncorect base code"):
        service.convert(Money(base="USDD", value=4.4), "EUR")


def test_convert_raises_for_non_200_response(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "app.infra.services.currency.requests.get",
        lambda *args, **kwargs: _FakeResponse(status_code=503, payload={}),
    )
    service = CurrencyConvertorClient()

    with pytest.raises(RuntimeError, match="Currency service error"):
        service.convert(Money(base="USD", value=4.4), "EUR")


def test_convert_uses_response_rate_for_requested_target_currency(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: dict[str, object] = {}

    def fake_get(url: str, *, params: dict[str, str]) -> _FakeResponse:
        calls["url"] = url
        calls["params"] = params
        return _FakeResponse(status_code=200, payload={"rates": {"EUR": 0.91}})

    monkeypatch.setattr("app.infra.services.currency.requests.get", fake_get)
    service = CurrencyConvertorClient()

    converted = service.convert(Money(base="USD", value=4.4), "EUR")

    assert calls == {
        "url": service.base_url,
        "params": {"base": "USD", "symbols": "EUR"},
    }
    assert converted.base == "EUR"
    assert converted.value == pytest.approx(4.004)
