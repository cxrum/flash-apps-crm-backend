from typing import Protocol

from app.modules.crm.application.admin.ingestion.commands import ListClickLogsCommand, ListEventLogsCommand
from app.modules.crm.application.admin.ingestion.responses import ListClickLogsResponse, ListRawEventsResponse


class IngestionDataServiceProtocol(Protocol):
    def list_clicks(self, command: ListClickLogsCommand) -> ListClickLogsResponse: ...
    def list_raw_events(self, command: ListEventLogsCommand) -> ListRawEventsResponse: ...
