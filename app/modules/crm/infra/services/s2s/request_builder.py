import asyncio
from typing import Protocol

import requests
from requests import Response

from app.modules.crm.application.base import JsonDict
from app.modules.crm.application.contracts.requester import S2SRequesterProtocol, S2SResponse


class RequestStrategy(Protocol):
    def execute(self, url: str, headers: JsonDict, params: JsonDict | None = None) -> Response: ...


class GetRequestStrategy(RequestStrategy):
    def execute(self, url: str, headers: JsonDict, params: JsonDict | None = None) -> Response:
        return requests.get(url, params=params, headers=headers)


class PostRequestStrategy(RequestStrategy):
    def execute(self, url: str, headers: JsonDict, params: JsonDict | None = None) -> Response:
        return requests.post(url, json=params, headers=headers)


class RequestStrategyFactory:
    @staticmethod
    def from_http_method(http_method: str) -> RequestStrategy:
        if http_method == "GET":
            return GetRequestStrategy()
        elif http_method == "POST":
            return PostRequestStrategy()

        return PostRequestStrategy()


class S2SRequester(S2SRequesterProtocol):
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
        strategy = RequestStrategyFactory.from_http_method(http_method)

        # TODO Implement retry_policy logic
        response = await self._execute_request(
            strategy=strategy,
            endpoint=url,
            base_url="",
            header=header,
            params=params,
            max_retries=max_retries,
            sleep_time=sleep_time,
        )

        status_code = response.status_code if response is not None else None

        return S2SResponse(is_success=status_code == 200)

    async def _execute_request(
        self,
        strategy: RequestStrategy,
        endpoint: str,
        base_url: str,
        header: JsonDict,
        params: JsonDict | None = None,
        max_retries: int = 5,
        sleep_time: int = 5,
    ) -> Response | None:
        attempt = 0
        url = f"{base_url}{endpoint}"

        while attempt < max_retries:
            try:
                response = strategy.execute(url, params=params, headers=header)
                response.raise_for_status()
                return response

            except requests.RequestException as e:
                attempt += 1
                if attempt == max_retries:
                    raise
                await asyncio.sleep(sleep_time)

        return None
