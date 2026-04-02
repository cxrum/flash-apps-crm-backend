from __future__ import annotations

from hashlib import sha256
import hmac

from app.domain.hash_protocol import HashableValue
from app.infra.services.signature import SignatureSHA256


def test_sign_returns_standard_hmac_sha256_digest() -> None:
    service = SignatureSHA256()
    value = HashableValue.from_str("message")
    key = HashableValue.from_str("secret")

    signature = service.sign(value=value, key=key)
    expected = hmac.new(key=b"secret", msg=b"message", digestmod=sha256).digest()

    assert signature.signature == HashableValue(expected)
    assert signature.signature.to_hex() == expected.hex()


def test_compare_returns_true_for_matching_signature() -> None:
    service = SignatureSHA256()
    value = HashableValue.from_str("message")
    key = HashableValue.from_str("secret")
    signature = service.sign(value=value, key=key)

    assert service.compare(value=value, signature=signature.signature, key=key) is True


def test_compare_returns_false_for_mismatched_signature() -> None:
    service = SignatureSHA256()
    value = HashableValue.from_str("message")
    key = HashableValue.from_str("secret")

    assert service.compare(
        value=value,
        signature=HashableValue.from_str("wrong-signature"),
        key=key,
    ) is False
