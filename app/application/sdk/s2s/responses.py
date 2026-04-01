

from dataclasses import dataclass

from app.application.base import BaseResponse


class S2SClickResponse(BaseResponse):
    click_id: str

