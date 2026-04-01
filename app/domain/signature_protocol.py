

from dataclasses import dataclass
from typing import Protocol

from app.domain.hash_protocol import HashedValue


@dataclass(frozen=True)
class SignatureValue:
    signature: HashedValue


class SignatureProtocol(Protocol):

    def sign(self, *, value: HashedValue, key: HashedValue) -> SignatureValue: ...
    def compare(self, *, value: HashedValue, signature: HashedValue, key: HashedValue) -> bool: ...