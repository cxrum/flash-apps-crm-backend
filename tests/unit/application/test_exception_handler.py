from __future__ import annotations

import asyncio
import json
import logging

import pytest
from fastapi import FastAPI, Request

from app.core.exception import BaseBoundaryException
from app.infra.exception import InfraGeneralException
from app.infra.exception_bus.handlers.stub import AsyncStubExceptionHandler
from app.application.exception import GeneralException
from app.core.config import settings
from app.di.dependencies import (
    build_exception_handler,
    get_exception_event_subscribers,
    register_fastapi_exception_handlers,
)
from app.domain.event_bus.entity import DomainEventMessage
from app.domain.event_bus.events.exception_event import ExceptionEvent


def build_exception_event(**payload_overrides: object) -> ExceptionEvent:
    payload = {
        "exception_type": "RuntimeError",
        "exception_message": "failed",
        "context": {"source": "worker"},
    }
    payload.update(payload_overrides)
    return ExceptionEvent(
        name=ExceptionEvent.EVENT_NAME,
        correlation_id="corr-1",
        payload=payload,
    )


class RecordingExceptionBus:
    def __init__(self) -> None:
        self.published_messages: list[ExceptionEvent] = []

    async def publish(self, message: ExceptionEvent) -> None:
        self.published_messages.append(message)


def build_request(
    *,
    path: str = "/api/v1/test",
    method: str = "GET",
    query_string: bytes = b"event_id=evt-1",
) -> Request:
    return Request(
        {
            "type": "http",
            "http_version": "1.1",
            "scheme": "http",
            "method": method,
            "path": path,
            "query_string": query_string,
            "headers": [],
            "client": ("127.0.0.1", 12345),
            "server": ("testserver", 80),
        }
    )


def test_async_stub_exception_handler_logs_exception_event(caplog: pytest.LogCaptureFixture) -> None:
    async def scenario() -> None:
        handler = AsyncStubExceptionHandler()
        message = build_exception_event(context={"source": "sdk", "event_id": "evt-1"})

        with caplog.at_level(
            logging.ERROR,
            logger="app.application.exception_bus.handlers.stub",
        ):
            await handler.handle(message)

        assert len(caplog.records) == 1
        record = caplog.records[0]
        assert record.message == "Stub exception handler received RuntimeError: failed"
        assert record.correlation_id == "corr-1"
        assert record.event_name == ExceptionEvent.EVENT_NAME
        assert record.exception_context == {"source": "sdk", "event_id": "evt-1"}

    asyncio.run(scenario())


def test_async_stub_exception_handler_rejects_non_exception_messages() -> None:
    async def scenario() -> None:
        handler = AsyncStubExceptionHandler()

        with pytest.raises(
            InfraGeneralException,
            match="AsyncStubExceptionHandler expected ExceptionEvent, got DomainEventMessage",
        ):
            await handler.handle(DomainEventMessage(name="crm.events.saved"))

    asyncio.run(scenario())


def test_get_exception_event_subscribers_includes_stub_handler() -> None:
    subscriber_map = {
        event_name: type(handler)
        for event_name, handler in get_exception_event_subscribers()
    }

    assert subscriber_map == {
        ExceptionEvent.EVENT_NAME: AsyncStubExceptionHandler,
    }


def test_build_fastapi_exception_handler_publishes_exception_event_and_returns_500() -> None:
    async def scenario() -> None:
        bus = RecordingExceptionBus()
        original_debug_mode = settings.debug_mode
        settings.debug_mode = False
        handler = build_exception_handler(bus)

        try:
            response = await handler(build_request(), RuntimeError("boom"))

            assert response.status_code == 500
            assert json.loads(response.body) == {"detail": "Internal server error"}
            assert len(bus.published_messages) == 1

            message = bus.published_messages[0]
            assert message.exception_type == "RuntimeError"
            assert message.exception_message == "boom"
            assert message.context == {
                "method": "GET",
                "path": "/api/v1/test",
                "query_params": {"event_id": "evt-1"},
                "client_host": "127.0.0.1",
            }
        finally:
            settings.debug_mode = original_debug_mode

    asyncio.run(scenario())


def test_register_fastapi_exception_handlers_registers_generic_exception_handler() -> None:
    app = FastAPI()
    bus = RecordingExceptionBus()

    register_fastapi_exception_handlers(app, bus)

    assert BaseBoundaryException in app.exception_handlers
