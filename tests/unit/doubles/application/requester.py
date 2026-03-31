from __future__ import annotations

from urllib.parse import urlencode

from app.application.contracts.requester import S2SRequesterProtocol, S2SResponse
from tests.unit.doubles.base import CallRecorderMixin


class StubS2SRequester(CallRecorderMixin, S2SRequesterProtocol):
    def __init__(self) -> None:
        super().__init__()
        self.response = S2SResponse(is_success=True)
        self.error: Exception | None = None
        self.final_urls: list[str] = []

    @staticmethod
    def _build_final_url(
        url: str,
        http_method: str,
        params: dict | None,
    ) -> str:
        if http_method != "GET" or not params:
            return url

        separator = "&" if "?" in url else "?"
        return f"{url}{separator}{urlencode(params, doseq=True)}"

    async def postback(
        self,
        url: str,
        http_method: str,
        header: dict,
        auth: dict,
        params: dict | None = None,
        retry_policy: str = "",
        max_retries: int = 5,
        sleep_time: int = 5,
    ) -> S2SResponse:
        self.final_urls.append(self._build_final_url(url, http_method, params))
        self._record(
            "postback",
            url,
            http_method,
            header,
            auth,
            params,
            retry_policy,
            max_retries,
            sleep_time,
        )
        if self.error is not None:
            raise self.error
        return self.response
