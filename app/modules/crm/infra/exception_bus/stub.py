from app.core.bus.exception.stub import AsyncStubExceptionHandler as CoreAsyncStubExceptionHandler
from app.core.exception import BusException
from app.modules.crm.infra.exception import BaseInfraException


class AsyncStubExceptionHandler(CoreAsyncStubExceptionHandler):
    async def handle(self, message: object) -> None:
        try:
            await super().handle(message)
        except BusException as exc:
            raise BaseInfraException(str(exc)) from exc
