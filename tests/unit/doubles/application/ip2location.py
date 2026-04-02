from __future__ import annotations

from app.application.contracts.ip2location import IP2LocationGatewayProtocol, IpLocation
from tests.unit.doubles.base import CallRecorderMixin


class StubIP2LocationGateway(CallRecorderMixin, IP2LocationGatewayProtocol):
    def __init__(self) -> None:
        super().__init__()
        self.default_location = IpLocation(
            city="Kyiv",
            country="Ukraine",
            country_code="UA",
            region="Kyiv City",
            language="uk",
        )
        self.locations_by_ip: dict[str, IpLocation] = {}

    def seed(self, *, ip: str, location: IpLocation) -> None:
        self.locations_by_ip[ip] = location

    def resolve(self, ip: str) -> IpLocation:
        self._record("resolve", ip)
        return self.locations_by_ip.get(ip, self.default_location)
