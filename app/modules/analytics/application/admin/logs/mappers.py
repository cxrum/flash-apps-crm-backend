from app.modules.analytics.domain.click.AnalyticsClickEntity import AnalyticsClickEntity
from app.modules.analytics.domain.events.AnalyticsEventEntity import AnalyticsEventEntity
from app.modules.crm.application.admin.logs.responses import ClickLogResponseEntry, RawEventLogResponseEntry


class AnalyticsLogsCommandsMapper:
    @classmethod
    def click_log_domain_to_value(cls, domain: AnalyticsClickEntity) -> ClickLogResponseEntry:
        return ClickLogResponseEntry.model_validate(domain)

    @classmethod
    def event_log_domain_to_value(cls, domain: AnalyticsEventEntity) -> RawEventLogResponseEntry:
        return RawEventLogResponseEntry.model_validate(domain)
