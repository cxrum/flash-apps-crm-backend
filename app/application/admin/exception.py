from typing import Any, Dict

from app.application.exception import GeneralException
from app.core.exception_resolver import MessageResolver


class AdminException(GeneralException):
    def __init__(self, message_key: str = "internal", context: Dict[str, Any]={}, code: int=500):
        super().__init__(message_key, context, code)
        self.args = (MessageResolver().resolve(message_key, context),)


class ClickNotFound(AdminException):
    def __init__(self, click_id: str):
        super().__init__("admin.click.not_found", {"click_id": click_id}, 404)
    

class EventNotFound(AdminException):
    def __init__(self, event_id: str):
        super().__init__("admin.event.not_found", {"event_id": event_id}, 404)
    

class InstallNotFound(AdminException):
    def __init__(self, click_id: str | None = None):
        context = {"click_id": click_id} if click_id is not None else {}
        super().__init__("admin.install.not_found", context, 404)
    
