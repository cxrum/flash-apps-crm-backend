import hmac
from hashlib import sha256

from app.core.config import settings


class SignatureVerifier:
    @staticmethod
    def verify_signature(app_secret: bytes, raw: bytes, signature: str) -> bool:
        received = signature.strip()
        if received.lower().startswith("sha256="):
            received = received.split("=", 1)[1]
        expected = SignatureVerifier.get_signature(app_secret, raw)
        return hmac.compare_digest(expected, received)

    @staticmethod
    def get_signature(app_secret: bytes, raw: bytes) -> str:
        return hmac.new(app_secret, raw, sha256).hexdigest()
