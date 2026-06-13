
from dataclasses import dataclass
from typing import Protocol

@dataclass
class S2SResponse:
    is_success: bool

class S2SRequesterProtocol(Protocol):
    async def postback(
        self, 
        url: str,
        http_method: str,
        header: dict,
        auth: dict,
        params: dict | None = None,
        retry_policy: str = "",
        max_retries: int = 5,
        sleep_time: int = 5
        ) -> S2SResponse: ...