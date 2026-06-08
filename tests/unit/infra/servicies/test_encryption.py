from __future__ import annotations

import pytest

from app.infra.services.encryption import EncryptionService


def test_encrypt_and_decrypt_round_trip() -> None:
    service = EncryptionService(secret="test-secret")
    encrypted = service.encrypt("secret")

    assert encrypted.startswith("enc::v1:")
    assert encrypted != "secret"
    assert service.decrypt(encrypted) == "secret"


def test_decrypt_supports_legacy_prefixed_values() -> None:
    service = EncryptionService(secret="test-secret")

    assert service.decrypt("enc::secret") == "secret"


def test_decrypt_rejects_tampered_payload() -> None:
    service = EncryptionService(secret="test-secret")
    encrypted = service.encrypt("secret")
    tampered = encrypted[:-1] + ("A" if encrypted[-1] != "A" else "B")

    with pytest.raises(ValueError, match="integrity check failed|Invalid encrypted payload"):
        service.decrypt(tampered)
