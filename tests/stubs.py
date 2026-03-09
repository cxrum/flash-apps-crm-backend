from datetime import datetime


class StubEventsRepository:
    def insert_events(self, events: list[object]) -> int:
        return len(events)


class StubIdentityRepository:
    def upsert_identities(self, identity_links: dict[str, str | None]) -> None:
        return None


class StubUserRepository:
    def upsert_users(self, user_ids: list[str], *, created_at: object | None = None) -> None:
        return None


class StubAppRepository:
    def exists(self, app_id: int) -> bool:
        return True


class StubRepositoryFactory:
    def app_repo(self, session: object) -> StubAppRepository:
        return StubAppRepository()

    def user_repo(self, session: object) -> StubUserRepository:
        return StubUserRepository()

    def identity_repo(self, session: object) -> StubIdentityRepository:
        return StubIdentityRepository()

    def event_repo(self, session: object) -> StubEventsRepository:
        return StubEventsRepository()

    def subscription_repo(self, session: object) -> object:
        raise NotImplementedError


class FailingEventsRepository:
    def insert_events(self, events: list[object]) -> int:
        raise RuntimeError("insert failed")


class StubFallingRepositoryFactory:
    def app_repo(self, session: object) -> StubAppRepository:
        return StubAppRepository()

    def user_repo(self, session: object) -> StubUserRepository:
        return StubUserRepository()

    def identity_repo(self, session: object) -> StubIdentityRepository:
        return StubIdentityRepository()

    def event_repo(self, session: object) -> FailingEventsRepository:
        return FailingEventsRepository()

    def subscription_repo(self, session: object) -> object:
        raise NotImplementedError


class FailingIdentityRepository:
    def upsert_user(self, user_id: str) -> None:
        return None

    def upsert_identity(self, *, anonymous_id: str, user_id: str, linked_at: datetime) -> None:
        raise RuntimeError("identity upsert failed")

    def upsert_identities(self, identity_links: dict[str, str | None]) -> None:
        return None


class IdentityOnlyRepositoryFactory:
    def app_repo(self, session: object) -> object:
        raise NotImplementedError

    def user_repo(self, session: object) -> object:
        raise NotImplementedError

    def identity_repo(self, session: object) -> FailingIdentityRepository:
        return FailingIdentityRepository()

    def event_repo(self, session: object) -> object:
        raise NotImplementedError

    def subscription_repo(self, session: object) -> object:
        raise NotImplementedError


class StubSession:
    def __init__(self) -> None:
        self.commit_calls = 0
        self.rollback_calls = 0
        self.close_calls = 0

    def commit(self) -> None:
        self.commit_calls += 1

    def rollback(self) -> None:
        self.rollback_calls += 1

    def close(self) -> None:
        self.close_calls += 1