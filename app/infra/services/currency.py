from copy import copy

import requests

from app.domain.currency.currency_convertor_protocol import CurrencyConvertorClientProtocol
from app.domain.currency.entity import Money


class CurrencyConvertorClient(CurrencyConvertorClientProtocol):
    
    def __init__(self) -> None:
        self.base_url = 'https://api.frankfurter.dev/v1/latest'
        super().__init__()
    
    
    def convert(self, _from: Money, _to: str) -> Money:
        
        if _from.base == _to:
            return copy(_from)
         
        if len(_to) != 3 or len(_from.base) != 3:
            raise RuntimeError("Inncorect base code")
            
        
        res = requests.get(
            self.base_url,
            params={
                "base": _from.base,
                "symbols": _to
            } 
        )
        
        if res.status_code != 200:
            raise RuntimeError("Currency service error")
        
        data = res.json()
        
        return Money(
            base=_to,
            value=_from.value * float(data["rates"][_to])
        )
        
        
