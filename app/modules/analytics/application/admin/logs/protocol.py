from typing import Protocol

from app.modules.crm.application.admin.logs.commands import ListClickLogsCommand, ListEventLogsCommand
from app.modules.crm.application.admin.logs.responses import ListClickLogsResponse, ListRawEventsResponse


class AnalyticsLogsServiceProtocol(Protocol):
    def list_clicks(self, command: ListClickLogsCommand) -> ListClickLogsResponse: ...
    def list_raw_events(self, command: ListEventLogsCommand) -> ListRawEventsResponse: ...
