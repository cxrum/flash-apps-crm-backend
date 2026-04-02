from __future__ import annotations

import pytest

from app.infra.services.encryption import EncryptionService


def test_encrypt_raises_not_implemented() -> None:
    service = EncryptionService()

    with pytest.raises(NotImplementedError):
        service.encrypt("secret")


def test_decrypt_raises_not_implemented() -> None:
    service = EncryptionService()

    with pytest.raises(NotImplementedError):
        service.decrypt("enc::secret")
