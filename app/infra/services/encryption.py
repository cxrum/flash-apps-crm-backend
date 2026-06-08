from __future__ import annotations

import base64
import hashlib
import os
from binascii import Error as BinasciiError

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from app.application.contracts.encryption import EncryptionServiceProtocol


class EncryptionService(EncryptionServiceProtocol):
    _PREFIX = "enc::"
    _VERSION = "v1"
    _NONCE_SIZE = 12
    _AAD = b"crm-app-secrets"

    def __init__(self, secret: str | None = None) -> None:
        if secret is None:
            from app.core.config import settings

            secret = settings.app_secret

        self._cipher = AESGCM(self._build_key(secret))

    def encrypt(self, value: str) -> str:
        nonce = os.urandom(self._NONCE_SIZE)
        ciphertext = self._cipher.encrypt(nonce, value.encode("utf-8"), self._AAD)
        payload = base64.urlsafe_b64encode(nonce + ciphertext).decode("ascii")
        return f"{self._PREFIX}{self._VERSION}:{payload}"

    def decrypt(self, value: str) -> str:
        if not value.startswith(self._PREFIX):
            return value

        payload = value[len(self._PREFIX) :]
        version_prefix = f"{self._VERSION}:"

        if not payload.startswith(version_prefix):
            return payload

        encoded_payload = payload[len(version_prefix) :]

        try:
            decoded_payload = base64.urlsafe_b64decode(encoded_payload.encode("ascii"))
        except (BinasciiError, ValueError) as exc:
            raise ValueError("Invalid encrypted payload") from exc

        if len(decoded_payload) <= self._NONCE_SIZE:
            raise ValueError("Invalid encrypted payload")

        nonce = decoded_payload[: self._NONCE_SIZE]
        ciphertext = decoded_payload[self._NONCE_SIZE :]

        try:
            plaintext = self._cipher.decrypt(nonce, ciphertext, self._AAD)
        except InvalidTag as exc:
            raise ValueError("Encrypted payload integrity check failed") from exc

        return plaintext.decode("utf-8")

    @staticmethod
    def _build_key(secret: str) -> bytes:
        return hashlib.sha256(secret.encode("utf-8")).digest()
