import IP2Location

from app.core.config import settings
from app.modules.crm.application.contracts.ip2location import IP2LocationGatewayProtocol, IpLocation


class IP2LocationGateway(IP2LocationGatewayProtocol):
    def __init__(self, database_path: str) -> None:
        self.path = database_path
        self.database = IP2Location.IP2Location(self.path)

    def resolve(self, ip: str) -> IpLocation:

        record = self.database.get_all(ip)

        if record is None:
            return IpLocation()

        return IpLocation(
            city=record.city,
            country=record.country_long,
            country_code=record.country_short,
        )
