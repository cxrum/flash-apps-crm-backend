from __future__ import annotations

import hashlib
import hmac
import json
from dataclasses import dataclass

import pytest
from fastapi.testclient import TestClient

from app.api.v1.events import _is_rate_limited
from app.application.events.entities import EventItemCommand, EventsBatchCommand, IngestEventsBatchCommand
from app.application.events.event_usecases import EventUseCases
from app.core.config import settings
from app.core.signature import SignatureVerifirer
from app.di.dependencies import get_event_usecases
from app.domain.events.service import BatchIngestResult, DomainAppNotFoundError
from app.infra.db.postgres_uow import SqlAlchemyUnitOfWork
from app.main import app
from tests.factories import EventPayloadFactory, EventsPayloadFactory
from tests.stubs import StubFallingRepositoryFactory, StubRepositoryFactory, StubSession

FAKE_APP_SECRET = "abracadabra228%!11".encode("utf-8")

@dataclass
class StubEventUseCases:
    result: BatchIngestResult | None = None
    error: Exception | None = None

    def process_batch(self, command: IngestEventsBatchCommand) -> BatchIngestResult:
        if self.error is not None:
            raise self.error
        if self.result is None:
            raise RuntimeError("Stub result was not provided")
        return self.result


def test_events_batch_api_success() -> None:
    use_case_stub = StubEventUseCases(
        result=BatchIngestResult(
            status="accepted",
            received=1,
            inserted=1,
            ignored_duplicates=0,
        )
    )
    app.dependency_overrides[get_event_usecases] = lambda: use_case_stub

    payload = EventsPayloadFactory.build()
    raw_body = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

    try:
        with TestClient(app) as client:
            response = client.post(
                "/v1/events/batch",
                content=raw_body,
                headers={
                    "Content-Type": "application/json",
                    "X-App-Id": "1",
                    "X-Env": "prod",
                    "X-Signature": SignatureVerifirer.get_signature(raw_body, settings.app_secret.encode("utf-8")),
                },
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 202
    assert response.json() == {
        "status": "accepted",
        "received": 1,
        "inserted": 1,
        "ignored_duplicates": 0,
    }


def test_events_batch_api_request_overflow() -> None:
    N = settings.batch_rate_limit_per_window + 1
    results1: list = []
    results2: list = []
    results3: list = []
    
    try:
        for i in range(0, N):
            results1.append(_is_rate_limited(1, "127.0.0.1"))
            results2.append(_is_rate_limited(2, "127.0.0.1"))
            results3.append(_is_rate_limited(1, "127.0.0.2"))
                
    except:
        pytest.fail("The method implemethed not correctly")
    
    for i, res in enumerate(zip(results1, results2, results3)):
        res1, res2, res3 = res
        
        if i < N-1:
            assert not res1
            assert not res2
            assert not res3
        else:
            assert res1
            assert res2
            assert res3
     

def test_events_batch_api_401_signature_error() -> None:
    use_case_stub = StubEventUseCases(
        result=BatchIngestResult(
            status="accepted",
            received=1,
            inserted=1,
            ignored_duplicates=0,
        )
    )
    app.dependency_overrides[get_event_usecases] = lambda: use_case_stub

    payload = EventsPayloadFactory.build()
    raw_body = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

    try:
        with TestClient(app) as client:
            response = client.post(
                "/v1/events/batch",
                content=raw_body,
                headers={
                    "Content-Type": "application/json",
                    "X-App-Id": "1",
                    "X-Env": "prod",
                    "X-Signature": SignatureVerifirer.get_signature(raw_body, FAKE_APP_SECRET),
                },
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid signature"

def test_events_batch_api_returns_404_on_unknown_app() -> None:
    use_case_stub = StubEventUseCases(error=DomainAppNotFoundError("Unknown app id"))
    app.dependency_overrides[get_event_usecases] = lambda: use_case_stub

    payload = EventsPayloadFactory.build()
    raw_body = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

    try:
        with TestClient(app) as client:
            response = client.post(
                "/v1/events/batch",
                content=raw_body,
                headers={
                    "Content-Type": "application/json",
                    "X-App-Id": "1",
                    "X-Env": "prod",
                    "X-Signature": SignatureVerifirer.get_signature(raw_body, settings.app_secret.encode("utf-8")),
                },
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 404
    assert response.json()["detail"] == "Unknown app id"


def test_events_use_case_rolls_back_transaction_on_repository_error() -> None:
    session = StubSession()
    uow = SqlAlchemyUnitOfWork(lambda: session)  # type: ignore[arg-type]
    use_cases = EventUseCases(uow=uow, repository_factory=StubFallingRepositoryFactory()) # type: ignore
    payload = EventsBatchCommand.model_validate(EventsPayloadFactory.build())
    command = IngestEventsBatchCommand(
        app_id=1,
        env="prod",
        signature="unused",
        payload=payload,
    )

    with pytest.raises(RuntimeError, match="insert failed"):
        result = use_cases.process_batch(command)

    assert session.commit_calls == 0
    assert session.rollback_calls == 1
    assert session.close_calls == 1


def test_events_use_case_succes() -> None:
    session = StubSession()
    uow = SqlAlchemyUnitOfWork(lambda: session)  # type: ignore[arg-type]
    use_cases = EventUseCases(uow=uow, repository_factory=StubRepositoryFactory()) # type: ignore
    payload = EventsBatchCommand.model_validate(EventsPayloadFactory.build())
    
    for i in range(0, 10):
        payload.events.append(EventItemCommand.model_validate(EventPayloadFactory.build()))
    
    event_N = len(payload.events)
    
    command = IngestEventsBatchCommand(
        app_id=1,
        env="prod",
        signature="unused",
        payload=payload,
    )

    result = use_cases.process_batch(command)
    
    assert result.inserted == event_N
    assert session.commit_calls == 1
    assert session.rollback_calls == 0
    assert session.close_calls == 1
