from typing import Callable

from sqlalchemy.orm import Session


class TrackingController:
    def __init__(
        self,
        session_factory: Callable[[], Session],
    ) -> None:
        self.session_factory = session_factory
