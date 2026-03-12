

from app.domain.uow import CrmUnitOfWorkProtocol


class EventLogObserver:
    
    def __init__(
        self, 
        uow: CrmUnitOfWorkProtocol
        ) -> None:
        self._uow = uow
    
    
    # TODO Sends to subscribres (in our case WorkerPool) recived event.    
    def create_log(self, **kargs):
        raise NotImplementedError