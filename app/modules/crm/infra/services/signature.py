import hmac
from hashlib import sha256

from app.modules.crm.domain.hash_protocol import HashableValue
from app.modules.crm.domain.signature_protocol import SignatureProtocol, SignatureValue


class SignatureSHA256(SignatureProtocol):
    def sign(self, *, value: HashableValue, key: HashableValue) -> SignatureValue:
        signature = hmac.new(
            key=key.bvalue,
            msg=value.bvalue,
            digestmod=sha256,
        ).digest()

        return SignatureValue(signature=HashableValue(signature))

    def compare(self, *, value: HashableValue, signature: HashableValue, key: HashableValue) -> bool:
        expected_signature = self.sign(value=value, key=key).signature.bvalue

        return hmac.compare_digest(
            expected_signature,
            signature.bvalue,
        )
