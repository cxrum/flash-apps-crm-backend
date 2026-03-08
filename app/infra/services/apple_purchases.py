from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol



class PurchasesClientProtocol(Protocol):
    def verify(self, id: str, **args) -> bool: ... 
    
    
class ApplePurchasesService(PurchasesClientProtocol):
    
    def __init__(self) -> None:
        super().__init__()
        
    def verify(self, id: str, **args) -> bool:
        return True