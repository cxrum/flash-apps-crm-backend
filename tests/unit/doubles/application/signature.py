from __future__ import annotations

from hashlib import sha256
import hmac

from app.domain.hash_protocol import HashableValue
from app.domain.signature_protocol import SignatureProtocol, SignatureValue
from tests.unit.doubles.base import CallRecorderMixin


class StubSignatureService(CallRecorderMixin, SignatureProtocol):
    def __init__(self) -> None:
        super().__init__()
        self.compare_result: bool | None = None

    def sign(self, *, value: HashableValue, key: HashableValue) -> SignatureValue:
        self._record("sign", value, key)
        digest = hmac.new(key=key.bvalue, msg=value.bvalue, digestmod=sha256).digest()
        return SignatureValue(signature=HashableValue(digest))

    def compare(self, *, value: HashableValue, signature: HashableValue, key: HashableValue) -> bool:
        self._record("compare", value, signature, key)
        if self.compare_result is not None:
            return self.compare_result
        expected = self.sign(value=value, key=key)
        return hmac.compare_digest(expected.signature.bvalue, signature.bvalue)
