from __future__ import annotations

import pytest

from app.domain.hash_protocol import HashableValue
from app.infra.services.hashing import ServerHash


def test_hash_value_returns_distinct_hash_and_compare_accepts_match() -> None:
    raw_value = HashableValue.from_str("server-secret")

    hashed = ServerHash.hash_value(raw_value)

    assert hashed != raw_value
    assert ServerHash.compare_hash(raw_value, hashed) is True


def test_compare_hash_rejects_mismatch() -> None:
    hashed = ServerHash.hash_value(HashableValue.from_str("server-secret"))

    assert ServerHash.compare_hash(HashableValue.from_str("different-secret"), hashed) is False
