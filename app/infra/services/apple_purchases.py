from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.domain.purchases.app_puchases_protocol import PurchasesClientProtocol

class ApplePurchasesService(PurchasesClientProtocol):
    
    def __init__(self) -> None:
        super().__init__()
        
    def verify(self, id: str, **args) -> bool:
        return True