import hmac
from hashlib import sha256

from app.modules.analytics.domain.signature_protocol import AnalyticsSignatureProtocol, AnalyticsSignatureValue
from app.modules.crm.domain.hash_protocol import HashableValue


class AnalyticsSignatureSHA256(AnalyticsSignatureProtocol):
    def sign(self, *, value: HashableValue, key: HashableValue) -> AnalyticsSignatureValue:
        signature = hmac.new(
            key=key.bvalue,
            msg=value.bvalue,
            digestmod=sha256,
        ).digest()
        return AnalyticsSignatureValue(signature=HashableValue(signature))

    def compare(self, *, value: HashableValue, signature: HashableValue, key: HashableValue) -> bool:
        expected_signature = self.sign(value=value, key=key).signature.bvalue
        return hmac.compare_digest(expected_signature, signature.bvalue)
