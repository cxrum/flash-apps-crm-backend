from app.modules.analytics.application.logs.contracts import AnalyticsClickLog, AnalyticsEventLog
from app.modules.analytics.domain.click.AnalyticsClickEntity import AnalyticsClickEntity
from app.modules.analytics.domain.events.AnalyticsEventEntity import AnalyticsEventEntity


class AnalyticsLogsMapper:
    @classmethod
    def click_log_from_domain(cls, domain: AnalyticsClickEntity) -> AnalyticsClickLog:
        return AnalyticsClickLog(
            click_id=domain.click_id,
            app_platform_id=domain.app_platform_id,
            status=domain.status,
            raw_query=dict(domain.raw_query),
            ip_address=domain.ip_address,
            user_agent=domain.user_agent,
            referrer=domain.referrer,
            source=domain.source,
            redirect_target=domain.redirect_target,
            normalized_params=dict(domain.normalized_params),
            created_at=domain.created_at,
        )

    @classmethod
    def event_log_from_domain(cls, domain: AnalyticsEventEntity) -> AnalyticsEventLog:
        return AnalyticsEventLog(
            event_id=domain.event_id,
            click_id=domain.click_id,
            event_type=domain.event_type,
            event_key=domain.event_key,
            event_time_utc=domain.event_time_utc,
            app_user_id=domain.app_user_id,
            amount=domain.amount,
            currency=domain.currency,
            amount_usd=domain.amount_usd,
            payload=dict(domain.payload),
            created_at=domain.created_at,
        )
