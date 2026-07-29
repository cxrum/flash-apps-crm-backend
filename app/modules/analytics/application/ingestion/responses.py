from app.modules.crm.application.base import BaseResponse


class SdkInstallResponse(BaseResponse):
    click_id: str
    app_user_id: int | None = None
