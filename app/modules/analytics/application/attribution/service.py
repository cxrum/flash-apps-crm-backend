from app.modules.analytics.application.attribution.contracts import AnalyticsClickContext, AnalyticsPostbackContext
from app.modules.analytics.application.attribution.protocol import AnalyticsAttributionPort
from app.modules.analytics.domain.uow import AnalyticsUnitOfWorkFactoryProtocol


class AnalyticsAttributionService(AnalyticsAttributionPort):
    def __init__(self, uow_factory: AnalyticsUnitOfWorkFactoryProtocol) -> None:
        self._uow_factory = uow_factory

    def get_click_context(self, click_id: str) -> AnalyticsClickContext | None:
        with self._uow_factory.create() as uow:
            click = uow.click_repo.get_by_id(click_id)
            if click is None:
                return None
            install = uow.install_repo.get_by_click_id(click_id)

        return AnalyticsClickContext(
            click_id=click.click_id,
            app_platform_id=click.app_platform_id,
            install_id=None if install is None else install.install_id,
            app_user_id=None if install is None else install.app_user_id,
        )

    def get_postback_context(self, event_id: str) -> AnalyticsPostbackContext | None:
        with self._uow_factory.create() as uow:
            event = uow.event_repo.get_by_id(event_id)
            if event is None:
                return None
            click = uow.click_repo.get_by_id(event.click_id)
            if click is None:
                return None
            install = uow.install_repo.get_by_click_id(click.click_id)
            current_params = {
                current_param.param_key: current_param.current_value()
                for current_param in uow.current_param_repo.list_by_click_id(click.click_id)
            }

        return AnalyticsPostbackContext(
            event_id=event.event_id,
            click=AnalyticsClickContext(
                click_id=click.click_id,
                app_platform_id=click.app_platform_id,
                install_id=None if install is None else install.install_id,
                app_user_id=None if install is None else install.app_user_id,
            ),
            event_type=event.event_type,
            event_key=event.event_key,
            event_time_utc=event.event_time_utc,
            amount=event.amount,
            amount_usd=event.amount_usd,
            payload=dict(event.payload),
            current_params=current_params,
        )
