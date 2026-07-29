from __future__ import annotations

import asyncio

import pytest

from app.modules.analytics.application.ingestion.exception import (
    IdempotencyKeyProcessing,
    IdempotencyStateLost,
    InvalidInstallKey,
)
from app.modules.analytics.application.ingestion.service import IngestionService
from app.modules.crm.application.sdk.exception import ClickNotFound
from tests.unit.base import UnitTestContext
from tests.unit.builders import (
    build_app_entity,
    build_app_platform_entity,
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
        key = service._scope("install", command.install_key, command.idempotency_key)
        claim = await unit_test_context.idempotency_repository.acquire(key)

        assert claim.is_owner
        with pytest.raises(IdempotencyKeyProcessing) as error:
            await service.process_install(command)
        assert error.value.code == 409

    asyncio.run(scenario())


def test_completed_keys_are_accepted_as_no_ops_for_all_ingestion_operations(
    unit_test_context: UnitTestContext,
) -> None:
    async def scenario() -> None:
        service: IngestionService = unit_test_context.build_ingestion_service()
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


def test_failed_request_releases_its_processing_key(unit_test_context: UnitTestContext) -> None:
    async def scenario() -> None:
        service = unit_test_context.build_ingestion_service()
        command = build_sdk_install_command(install_key="missing-platform", idempotency_key="retryable-key")
        key = service._scope("install", command.install_key, command.idempotency_key)

        with pytest.raises(InvalidInstallKey):
            await service.process_install(command)

        retry = await unit_test_context.idempotency_repository.acquire(key)
        assert retry.is_owner

    asyncio.run(scenario())


def test_completed_install_skips_validation_and_persistence(unit_test_context: UnitTestContext) -> None:
    async def scenario() -> None:
        service = unit_test_context.build_ingestion_service()
        command = build_sdk_install_command(install_key="missing-platform", idempotency_key="completed-key")
        key = service._scope("install", command.install_key, command.idempotency_key)
        claim = await unit_test_context.idempotency_repository.acquire(key)

        assert claim.owner_token is not None
        assert await unit_test_context.idempotency_repository.complete(key, claim.owner_token)
        assert await service.process_install(command) is None
        assert unit_test_context.uow.enter_count == 0

    asyncio.run(scenario())


def test_failed_batches_and_parameter_updates_release_keys_for_retry(unit_test_context: UnitTestContext) -> None:
    async def scenario() -> None:
        service = unit_test_context.build_ingestion_service()
        batch = build_sdk_events_command(install_key="missing-platform", idempotency_key="batch-retry")
        batch_key = service._scope("events", f"{batch.install_key}:{batch.click_id}", batch.idempotency_key)

        with pytest.raises(InvalidInstallKey):
            await service.process_batch_events(batch)

        assert (await unit_test_context.idempotency_repository.acquire(batch_key)).is_owner

        params = build_sdk_params_update_command(click_id="missing-click", idempotency_key="params-retry")
        params_key = service._scope("params-update", params.click_id, params.idempotency_key)

        with pytest.raises(ClickNotFound):
            await service.update_params(params)

        assert (await unit_test_context.idempotency_repository.acquire(params_key)).is_owner

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
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def scenario() -> None:
        service = unit_test_context.build_ingestion_service()
        platform = _seed_platform(unit_test_context)
        command = build_sdk_install_command(click_id=None, install_key=platform.install_key, idempotency_key="lost-owner")
        key = service._scope("install", command.install_key, command.idempotency_key)

        async def complete_without_ownership(_: str, __: str) -> bool:
            return False

        monkeypatch.setattr(unit_test_context.idempotency_repository, "complete", complete_without_ownership)

        with pytest.raises(IdempotencyStateLost) as error:
            await service.process_install(command)

        assert error.value.code == 500
        assert not (await unit_test_context.idempotency_repository.acquire(key)).is_owner

    asyncio.run(scenario())
