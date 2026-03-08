
from hashlib import sha256
import hmac

from app.core.config import Settings


class SignatueVerifirer:
    
    @staticmethod
    def verify_signature(raw: bytes, signature: str) -> bool:
        received = signature.strip()
        if received.lower().startswith("sha256="):
            received = received.split("=", 1)[1]
        expected = hmac.new(Settings.app_secret.encode("utf-8"), raw, sha256).hexdigest()
        return hmac.compare_digest(expected, received)
    