from dataclasses import dataclass
from typing import Protocol

@dataclass
class IpLocation:
    city: str | None = None
    country: str | None = None
    country_code: str | None = None
    region: str | None = None
    language: str | None = None

class IP2LocationGatewayProtocol(Protocol):
    
    def resolve(self, ip: str) -> IpLocation: ...