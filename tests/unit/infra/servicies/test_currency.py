
import pytest

from app.infra.services.currency import CurrencyConvertorClient
from tests.unit.builders.entities import build_currency_entity


def test_currency_service():
    service = CurrencyConvertorClient()   
    
    uah = build_currency_entity(base = "UAH", value = 2.40)
    usd = build_currency_entity(base = "USD", value = 4.40)
    incorrect_usd = build_currency_entity(base = "U1SD", value = 4.40)
    
    with pytest.raises(RuntimeError, match="Currency service error"):
        uah_in_usd = service.convert(uah, "USD")
    
    with pytest.raises(RuntimeError, match="Inncorect base code"):
        uah_in_usd = service.convert(incorrect_usd, "USD")
    
    usd_in_euro = service.convert(usd, "EUR")
    
    assert usd_in_euro.base == "EUR"
    assert usd_in_euro.value < usd.value
    