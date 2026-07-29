from __future__ import annotations

import importlib
import inspect
from pathlib import Path

import pytest

from app.modules.crm.domain.uow import UnitOfWorkProtocol
from tests.unit.doubles.application.encryption import StubEncryptionService
from tests.unit.doubles.domain.uow import StubUnitOfWork
from tests.unit.doubles.registry import PROTOCOL_DOUBLE_REGISTRY


def _discover_protocol_types() -> set[type]:
    repo_root = Path(__file__).resolve().parents[2]
    crm_root = repo_root / "app" / "modules" / "crm"
    module_paths = list((crm_root / "domain").glob("*_protocol.py"))
    module_paths.extend((crm_root / "domain").glob("*/*_protocol.py"))
    module_paths.append(crm_root / "domain" / "uow.py")
    module_paths.extend((crm_root / "application" / "contracts").glob("*.py"))

    protocols: set[type] = set()
    for path in module_paths:
        if path.name == "__init__.py":
            continue
        module_name = ".".join(path.relative_to(repo_root).with_suffix("").parts)
        module = importlib.import_module(module_name)
        for name, value in vars(module).items():
            if inspect.isclass(value) and name.endswith("Protocol") and value.__module__ == module.__name__:
                protocols.add(value)
    return protocols


def test_protocol_registry_covers_all_current_application_and_domain_protocols() -> None:
    assert set(PROTOCOL_DOUBLE_REGISTRY) == _discover_protocol_types()


def test_stub_unit_of_work_exposes_full_protocol_surface() -> None:
    uow = StubUnitOfWork()

    for attribute_name in UnitOfWorkProtocol.__annotations__:
        assert hasattr(uow, attribute_name)

    assert hasattr(uow, "__enter__")
    assert hasattr(uow, "__exit__")
    assert hasattr(uow, "commit")
    assert hasattr(uow, "rollback")


def test_stub_unit_of_work_commits_on_clean_context_exit() -> None:
    uow = StubUnitOfWork()

    with uow as entered:
        assert entered is uow

    assert uow.enter_count == 1
    assert uow.exit_count == 1
    assert uow.commit_count == 1
    assert uow.rollback_count == 0


def test_stub_unit_of_work_rolls_back_on_error() -> None:
    uow = StubUnitOfWork()

    with pytest.raises(RuntimeError, match="boom"):
        with uow:
            raise RuntimeError("boom")

    assert uow.enter_count == 1
    assert uow.exit_count == 1
    assert uow.commit_count == 0
    assert uow.rollback_count == 1


def test_stub_encryption_service_records_calls_and_round_trips() -> None:
    encryption = StubEncryptionService()

    encrypted_value = encryption.encrypt("secret")
    decrypted_value = encryption.decrypt(encrypted_value)

    assert encrypted_value == "enc::secret"
    assert decrypted_value == "secret"
    assert [call.method for call in encryption.calls] == ["encrypt", "decrypt"]
