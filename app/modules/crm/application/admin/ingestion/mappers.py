from collections.abc import Mapping

from app.core.utils.general_mapper import GeneralMapper
from app.modules.crm.application.admin.ingestion.commands import ListClickLogsCommand, ListEventLogsCommand


class IngestionDataResponseMapper:
    @classmethod
    def click_logs_from_transport(cls, payload: Mapping[str, object]) -> ListClickLogsCommand:
        return GeneralMapper.command_payload_to_command(ListClickLogsCommand, payload)

    @classmethod
    def event_logs_from_transport(cls, payload: Mapping[str, object]) -> ListEventLogsCommand:
        return GeneralMapper.command_payload_to_command(ListEventLogsCommand, payload)
