from __future__ import annotations

import asyncio

import pytest

from app.modules.analytics.application.exception import AnalyticsClickNotFound
from app.modules.analytics.application.ingestion.exception import (
    IdempotencyKeyProcessing,
    IdempotencyStateLost,
    InvalidInstallKey,
)
from tests.unit.base import UnitTestContext
from tests.unit.builders import (
    build_app_entity,
    build_app_platform_entity,
    build_click_entity,
    build_sdk_event_command,
    build_sdk_events_command,
    build_sdk_install_command,
    build_sdk_params_update_command,
)


def _seed_platform(context: UnitTestContext):
    context.uow.app_repo.save(build_app_entity(app_id=1))
    return context.uow.app_platform_repo.save(build_app_platform_entity(app_id=1, install_key="install-key-ios"))


def test_processing_key_returns_conflict_before_the_request_is_processed(unit_test_context: UnitTestContext) -> None:
    async def scenario() -> None:
        service = unit_test_context.build_ingestion_service()
        command = build_sdk_install_command(idempotency_key="same-key")
        unit_test_context.idempotency_repository.return_processing_for_next_request()

        with pytest.raises(IdempotencyKeyProcessing) as error:
            await service.process_install(command)
        assert error.value.code == 409

    asyncio.run(scenario())


def test_completed_keys_are_accepted_as_no_ops_for_all_ingestion_operations(
    unit_test_context: UnitTestContext,
) -> None:
    async def scenario() -> None:
        service = unit_test_context.build_ingestion_service()
        platform = _seed_platform(unit_test_context)
        install = await service.process_install(
            build_sdk_install_command(click_id=None, install_key=platform.install_key, idempotency_key="install-key")
        )

        assert install is not None
        assert await service.process_install(
            build_sdk_install_command(click_id=None, install_key=platform.install_key, idempotency_key="install-key")
        ) is None

        events = build_sdk_events_command(
            click_id=install.click_id,
            install_key=platform.install_key,
            idempotency_key="batch-key",
            events=[build_sdk_event_command(idempotency_key="event-key")],
        )
        assert await service.process_batch_events(events)
        assert not await service.process_batch_events(events)

        params = build_sdk_params_update_command(click_id=install.click_id, idempotency_key="params-key")
        assert await service.update_params(params)
        assert not await service.update_params(params)

    asyncio.run(scenario())


def test_failed_install_can_be_retried_after_its_missing_platform_is_created(unit_test_context: UnitTestContext) -> None:
    async def scenario() -> None:
        service = unit_test_context.build_ingestion_service()
        command = build_sdk_install_command(click_id=None, idempotency_key="retryable-key")

        with pytest.raises(InvalidInstallKey):
            await service.process_install(command)

        _seed_platform(unit_test_context)
        assert await service.process_install(command) is not None

    asyncio.run(scenario())


def test_failed_batch_can_be_retried_after_its_missing_platform_is_created(unit_test_context: UnitTestContext) -> None:
    async def scenario() -> None:
        service = unit_test_context.build_ingestion_service()
        command = build_sdk_events_command(
            install_key="install-key-ios",
            click_id="retry-click",
            idempotency_key="batch-retry",
            events=[build_sdk_event_command(idempotency_key="retry-event")],
        )

        with pytest.raises(InvalidInstallKey):
            await service.process_batch_events(command)

        platform = _seed_platform(unit_test_context)
        unit_test_context.uow.click_repo.insert(
            build_click_entity(click_id=command.click_id, app_platform_id=platform.platform_id)
        )
        assert await service.process_batch_events(command)

    asyncio.run(scenario())


def test_failed_parameter_update_can_be_retried_after_its_click_is_created(unit_test_context: UnitTestContext) -> None:
    async def scenario() -> None:
        service = unit_test_context.build_ingestion_service()
        params = build_sdk_params_update_command(click_id="missing-click", idempotency_key="params-retry")

        with pytest.raises(AnalyticsClickNotFound):
            await service.update_params(params)

        unit_test_context.uow.click_repo.insert(build_click_entity(click_id=params.click_id))
        assert await service.update_params(params)

    asyncio.run(scenario())


def test_same_client_key_is_independent_for_each_ingestion_operation(
    unit_test_context: UnitTestContext,
) -> None:
    async def scenario() -> None:
        service = unit_test_context.build_ingestion_service()
        platform = _seed_platform(unit_test_context)
        shared_key = "shared-client-key"

        install = await service.process_install(
            build_sdk_install_command(
                click_id=None,
                install_key=platform.install_key,
                idempotency_key=shared_key,
            )
        )
        assert install is not None

        assert await service.process_batch_events(
            build_sdk_events_command(
                install_key=platform.install_key,
                click_id=install.click_id,
                idempotency_key=shared_key,
                events=[build_sdk_event_command(idempotency_key="batch-event-key")],
            )
        )
        assert await service.update_params(
            build_sdk_params_update_command(click_id=install.click_id, idempotency_key=shared_key)
        )

    asyncio.run(scenario())


def test_lost_idempotency_ownership_is_reported_after_processing(
    unit_test_context: UnitTestContext,
) -> None:
    async def scenario() -> None:
        service = unit_test_context.build_ingestion_service()
        platform = _seed_platform(unit_test_context)
        command = build_sdk_install_command(click_id=None, install_key=platform.install_key, idempotency_key="lost-owner")
        unit_test_context.idempotency_repository.fail_next_completion()

        with pytest.raises(IdempotencyStateLost) as error:
            await service.process_install(command)

        assert error.value.code == 500
        with pytest.raises(IdempotencyKeyProcessing):
            await service.process_install(command)

    asyncio.run(scenario())
