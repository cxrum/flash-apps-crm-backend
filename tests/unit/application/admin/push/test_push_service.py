import pytest

from app.modules.crm.application.admin.exception import ClickNotFound, InstallNotFound
from app.modules.crm.application.admin.push.commands import PushDeviceRegisterCommand
from app.modules.crm.application.admin.push.service import PushService
from app.modules.crm.application.attribution.contracts import CrmClickContext
from tests.unit.builders import build_app_entity, build_app_platform_entity
from tests.unit.doubles.domain.uow import StubUnitOfWork, StubUoWFactory


class _AttributionGatewayStub:
    def __init__(self, context: CrmClickContext | None) -> None:
        self.context = context

    def get_click_context(self, click_id: str) -> CrmClickContext | None:
        return self.context if self.context is not None and self.context.click_id == click_id else None

    def get_postback_context(self, event_id: str):
        raise AssertionError(f"Unexpected postback lookup: {event_id}")


class _AuthorizationStub:
    def required_user_permission(self, **_: object) -> None:
        return None


def _register_command() -> PushDeviceRegisterCommand:
    return PushDeviceRegisterCommand(
        install_key="install-key-ios",
        push_token="push-token-1",
        click_id="click-1",
        params={},
    )


def test_register_device_persists_a_token_from_the_attribution_port_context() -> None:
    uow = StubUnitOfWork()
    uow.app_repo.save(build_app_entity(app_id=1))
    uow.app_platform_repo.save(build_app_platform_entity(app_id=1, install_key="install-key-ios"))
    service = PushService(
        StubUoWFactory(uow),
        _AuthorizationStub(),  # type: ignore[arg-type]
        _AttributionGatewayStub(CrmClickContext("click-1", 1, 9, None)),  # type: ignore[arg-type]
    )

    service.register_device(_register_command())

    token = uow.push_token_repo.get_by_token("push-token-1")
    assert token is not None
    assert token.click_id == "click-1"
    assert token.install_id == 9


@pytest.mark.parametrize(
    ("context", "exception_type"),
    [
        pytest.param(None, ClickNotFound, id="click-missing"),
        pytest.param(CrmClickContext("click-1", 1, None, None), InstallNotFound, id="install-missing"),
    ],
)
def test_register_device_rejects_missing_attribution_references(
    context: CrmClickContext | None,
    exception_type: type[Exception],
) -> None:
    service = PushService(
        StubUoWFactory(StubUnitOfWork()),
        _AuthorizationStub(),  # type: ignore[arg-type]
        _AttributionGatewayStub(context),  # type: ignore[arg-type]
    )

    with pytest.raises(exception_type):
        service.register_device(_register_command())
