from dataclasses import dataclass
from typing import Protocol

from app.modules.crm.domain.hash_protocol import HashableValue


@dataclass(frozen=True)
class SignatureValue:
    signature: HashableValue


class SignatureProtocol(Protocol):
    def sign(self, *, value: HashableValue, key: HashableValue) -> SignatureValue: ...
    def compare(self, *, value: HashableValue, signature: HashableValue, key: HashableValue) -> bool: ...
