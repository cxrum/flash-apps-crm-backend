from __future__ import annotations

from app.domain.hash_protocol import HashProtocol, HashableValue
from tests.unit.doubles.base import CallRecorderMixin


class StubHashService(CallRecorderMixin, HashProtocol):
    def __init__(self) -> None:
        super().__init__()
        self._counter = 0

    def random_hash(self, lenb: int = 32) -> HashableValue:
        self._record("random_hash", lenb)
        self._counter += 1
        return HashableValue.from_str(f"random-hash-{lenb}-{self._counter}")

    def hash_value(self, value: HashableValue) -> HashableValue:
        self._record("hash_value", value)
        return HashableValue(b"hashed::" + value.bvalue)

    def compare_hash(self, raw_value: HashableValue, hash: HashableValue) -> bool:
        self._record("compare_hash", raw_value, hash)
        return hash.bvalue == b"hashed::" + raw_value.bvalue
