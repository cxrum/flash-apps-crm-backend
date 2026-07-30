from app.modules.analytics.application.attribution.contracts import AnalyticsClickContext, AnalyticsPostbackContext
from app.modules.analytics.application.attribution.protocol import AnalyticsAttributionPort
from app.modules.crm.application.attribution.contracts import CrmClickContext, CrmPostbackContext
from app.modules.crm.application.attribution.protocol import CrmAttributionGateway


class CrmAnalyticsAttributionAdapter(CrmAttributionGateway):
    def __init__(self, analytics_attribution: AnalyticsAttributionPort) -> None:
        self._analytics_attribution = analytics_attribution

    def get_click_context(self, click_id: str) -> CrmClickContext | None:
        context = self._analytics_attribution.get_click_context(click_id)
        return None if context is None else self._click_context(context)

    def get_postback_context(self, event_id: str) -> CrmPostbackContext | None:
        context = self._analytics_attribution.get_postback_context(event_id)
        if context is None:
            return None
        return CrmPostbackContext(
            event_id=context.event_id,
            click=self._click_context(context.click),
            event_type=context.event_type,
            event_key=context.event_key,
            event_time_utc=context.event_time_utc,
            amount=context.amount,
            amount_usd=context.amount_usd,
            payload=dict(context.payload),
            current_params=dict(context.current_params),
        )

    @staticmethod
    def _click_context(context: AnalyticsClickContext) -> CrmClickContext:
        return CrmClickContext(
            click_id=context.click_id,
            app_platform_id=context.app_platform_id,
            install_id=context.install_id,
            app_user_id=context.app_user_id,
        )
