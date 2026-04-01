import copy
from hashlib import sha256
import hmac

from app.domain.hash_protocol import HashedValue
from app.domain.signature_protocol import SignatureProtocol
from app.domain.signature_protocol import SignatureValue

class SignatureSHA256(SignatureProtocol):
    
    def sign(self, *, value: HashedValue, key: HashedValue) -> SignatureValue:
        signature = hmac.new(
            key=value.bvalue,
            msg=key.bvalue,
            digestmod=sha256
        ).hexdigest()
        
        return SignatureValue(
            signature=HashedValue.from_hex(signature)
        )
    
    def compare(self, *, value: HashedValue, signature: HashedValue, key: HashedValue) -> bool:
        _signature = hmac.new(
            key=value.bvalue,
            msg=key.bvalue,
            digestmod=sha256
        ).digest()
        
        return hmac.compare_digest(
            _signature,
            signature.bvalue
        )
