from typing import Any, Dict

from app.application.admin.exception import AdminException


class PushException(AdminException):
    def __init__(self, message_key: str = "internal", context: Dict[str, Any]={}, code: int = 500):
        super().__init__(message_key, context, code)


class InvalidScheduledAt(PushException):
    def __init__(self, value: str):
        super().__init__("admin.push.scheduled_at.invalid", {"value": value}, 400)


class PushCampaignNotFound(PushException):
    def __init__(self, push_id: int):
        super().__init__("admin.push.campaign.not_found", {"push_id": push_id}, 404)


class PushCampaignAppMismatch(PushException):
    def __init__(self, push_id: int, app_id: int):
        super().__init__("admin.push.campaign.app.mismatch", {"push_id": push_id, "app_id": app_id}, 404)


class PushPlatformNotFound(PushException):
    def __init__(self):
        super().__init__("admin.push.platform.not_found", {}, 404)


class PushAppUserNotFound(PushException):
    def __init__(self, app_user_id: int):
        super().__init__("admin.push.app_user.not_found", {"app_user_id": app_user_id}, 404)
