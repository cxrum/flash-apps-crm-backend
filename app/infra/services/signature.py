from hashlib import sha256
import hmac

from app.domain.hash_protocol import HashableValue
from app.domain.signature_protocol import SignatureProtocol
from app.domain.signature_protocol import SignatureValue

class SignatureSHA256(SignatureProtocol):
    
    def sign(self, *, value: HashableValue, key: HashableValue) -> SignatureValue:
        signature = hmac.new(
            key=key.bvalue,
            msg=value.bvalue,
            digestmod=sha256,
        ).digest()
        
        return SignatureValue(
            signature=HashableValue(signature)
        )
    
    def compare(self, *, value: HashableValue, signature: HashableValue, key: HashableValue) -> bool:
        expected_signature = self.sign(value=value, key=key).signature.bvalue
        
        return hmac.compare_digest(
            expected_signature,
            signature.bvalue,
        )
