from typing import Callable

from sqlalchemy.orm import Session

from app.modules.analytics.model.models import ClickModel
from app.modules.crm.infra.db.attribution.models import Click


class IngestionController:
    def __init__(
        self,
        session_factory: Callable[[], Session],
    ) -> None:
        self.session_factory = session_factory
