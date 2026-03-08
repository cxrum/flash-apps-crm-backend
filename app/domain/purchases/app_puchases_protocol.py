from typing import Protocol


class PurchasesClientProtocol(Protocol):
    def verify(self, id: str, **args) -> bool: ...