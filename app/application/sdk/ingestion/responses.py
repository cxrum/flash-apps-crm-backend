
from dataclasses import dataclass

from app.application.base import BaseResponse


class SdkInstallResponse(BaseResponse):
    click_id: str
    app_user_id: int | None = None


class SdkEventResponse(BaseResponse):
    received: int
    inserted: int
    
class SdkUpdateParamsResponse(BaseResponse):
    received: int
    inserted: int
    