from __future__ import annotations

from tests.unit.builders import (
    build_app_entity,
    build_app_platform_entity,
    build_app_secret_entity,
    build_click_entity,
    build_event_entity,
)
from tests.unit.doubles.domain.repositories.apps import InMemoryCrmAppPlatformRepository, InMemoryCrmAppRepository
from tests.unit.doubles.domain.repositories.attribution import InMemoryCrmClickRepository, InMemoryCrmEventRepository
from tests.unit.doubles.domain.repositories.config import InMemoryCrmAppSecretRepository


def test_app_repository_save_get_and_list_are_deterministic() -> None:
    repository = InMemoryCrmAppRepository()

    first = repository.save(build_app_entity(name="App One", code_slug="app-one"))
    second = repository.save(build_app_entity(name="App Two", code_slug="app-two"))

    assert repository.get_by_id(first.app_id or 0) == first
    assert repository.get_by_slug("app-two") == second
    assert [item.code_slug for item in repository.list_all()] == ["app-one", "app-two"]


def test_event_repository_ignores_duplicates_and_lists_by_app_id() -> None:
    app_platform_repo = InMemoryCrmAppPlatformRepository()
    saved_platform = app_platform_repo.save(build_app_platform_entity(app_id=7, platform="ios"))

    click_repo = InMemoryCrmClickRepository()
    click_repo.insert(build_click_entity(click_id="click-7", app_platform_id=saved_platform.platform_id or 0))

    repository = InMemoryCrmEventRepository(
        click_lookup=click_repo.get_by_id,
        platform_lookup=app_platform_repo.get_by_id,
    )

    inserted = repository.insert_many(
        [
            build_event_entity(event_id="evt-1", click_id="click-7"),
            build_event_entity(event_id="evt-1", click_id="click-7", event_key="duplicate"),
        ]
    )

    assert [item.event_id for item in inserted] == ["evt-1"]
    assert [item.event_id for item in repository.list_by_app_id(7)] == ["evt-1"]


def test_app_secret_repository_filters_by_app_platform_and_active_flag() -> None:
    app_platform_repo = InMemoryCrmAppPlatformRepository()
    ios_platform = app_platform_repo.save(build_app_platform_entity(app_id=1, platform="ios"))
    android_platform = app_platform_repo.save(
        build_app_platform_entity(app_id=1, platform="android", install_key="install-key-android")
    )

    repository = InMemoryCrmAppSecretRepository(platform_lookup=app_platform_repo.get_by_id)
    repository.save(
        build_app_secret_entity(
            secret_id=1,
            template_id=10,
            platform_id=ios_platform.platform_id,
            active_flag=True,
        )
    )
    repository.save(
        build_app_secret_entity(
            secret_id=2,
            template_id=11,
            platform_id=ios_platform.platform_id,
            active_flag=False,
        )
    )
    repository.save(
        build_app_secret_entity(
            secret_id=3,
            template_id=12,
            platform_id=android_platform.platform_id,
            active_flag=True,
        )
    )

    all_ios = repository.list_by_app_id(1, platform_id=ios_platform.platform_id)
    active_ios = repository.list_active_by_app(1, platform_id=ios_platform.platform_id)

    assert [item.secret_id for item in all_ios] == [1, 2]
    assert [item.secret_id for item in active_ios] == [1]
