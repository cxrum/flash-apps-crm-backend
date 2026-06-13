from typing import Callable

from sqlalchemy.orm import Session

from app.modules.analytics.model.models import CurrentParamModel
from app.modules.analytics.types.currentParam import CurrentParam


class AggregationController:
    def __init__(
        self,
        session_factory: Callable[[], Session],
    ) -> None:
        self.session_factory = session_factory
