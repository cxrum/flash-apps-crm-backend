from app.modules.crm.application.crm_authentication.responses import ResolvedCrmUserResponse
from app.modules.crm.di.dependencies import resolve_raw_logs_user
from app.modules.crm.domain.permission.CrmPermissionEntity import CrmPermissionEntity
from tests.unit.doubles.domain.uow import StubUnitOfWork, StubUoWFactory


class _AuthorizationRecorder:
    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []

    def required_user_permission(self, **kwargs: object) -> None:
        self.calls.append(kwargs)


def test_raw_logs_permission_is_checked_at_the_crm_boundary() -> None:
    uow = StubUnitOfWork()
    authorization = _AuthorizationRecorder()
    crm_user = ResolvedCrmUserResponse(crm_user_id=42)

    resolved_user = resolve_raw_logs_user(
        app_id=7,
        crm_user=crm_user,
        authorization_service=authorization,  # type: ignore[arg-type]
        uow_factory=StubUoWFactory(uow),
    )

    assert resolved_user == crm_user
    assert authorization.calls == [
        {
            "uow": uow,
            "crm_user_id": 42,
            "app_id": 7,
            "permission_code": CrmPermissionEntity.view_raw_logs_permission(),
        }
    ]
