from datetime import datetime

from app.core.bus.type import EventMessage


class UpdateCurrentParamMessage(EventMessage):
    EVENT_NAME = "sdk.update.current_params.request"

    @property
    def click_id(self) -> str:
        return str(self.payload["click_id"])

    @property
    def params(self) -> dict:
        return dict(self.payload["params"])

    @property
    def updated_at(self) -> datetime:
        value = self.payload["updated_at"]
        if not isinstance(value, datetime):
            raise Exception()  # TODO Change to bus exception
        return value
