from dataclasses import dataclass

from app.modules.crm.application.base import BaseResponse


class S2SClickResponse(BaseResponse):
    click_id: str
