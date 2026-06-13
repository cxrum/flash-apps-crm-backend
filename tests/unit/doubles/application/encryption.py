from __future__ import annotations

from app.modules.crm.application.contracts.encryption import EncryptionServiceProtocol
from tests.unit.doubles.base import CallRecorderMixin


class StubEncryptionService(CallRecorderMixin, EncryptionServiceProtocol):
    def __init__(self, *, prefix: str = "enc::") -> None:
        super().__init__()
        self.prefix = prefix
        self.encrypt_overrides: dict[str, str] = {}
        self.decrypt_overrides: dict[str, str] = {}

    def seed_encrypted_value(self, plain_value: str, encrypted_value: str) -> None:
        self.encrypt_overrides[plain_value] = encrypted_value
        self.decrypt_overrides[encrypted_value] = plain_value

    def seed_decrypted_value(self, encrypted_value: str, plain_value: str) -> None:
        self.decrypt_overrides[encrypted_value] = plain_value

    def encrypt(self, value: str) -> str:
        self._record("encrypt", value)
        if value in self.encrypt_overrides:
            return self.encrypt_overrides[value]
        encrypted_value = f"{self.prefix}{value}"
        self.decrypt_overrides.setdefault(encrypted_value, value)
        return encrypted_value

    def decrypt(self, value: str) -> str:
        self._record("decrypt", value)
        if value in self.decrypt_overrides:
            return self.decrypt_overrides[value]
        if value.startswith(self.prefix):
            return value[len(self.prefix) :]
        return value
