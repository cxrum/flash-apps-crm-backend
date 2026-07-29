from dataclasses import dataclass
from typing import Protocol

from app.modules.crm.domain.hash_protocol import HashableValue


@dataclass(frozen=True)
class AnalyticsSignatureValue:
    signature: HashableValue


class AnalyticsSignatureProtocol(Protocol):
    def sign(self, *, value: HashableValue, key: HashableValue) -> AnalyticsSignatureValue: ...
    def compare(self, *, value: HashableValue, signature: HashableValue, key: HashableValue) -> bool: ...
