from pydantic import Field

from app.application.base import FlexibleCommand


class ShareAppAccessCommand(FlexibleCommand):
    crm_user_id: int
    app_id: int
    manager_id: int
    role_code: str
