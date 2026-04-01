from app.application.contracts.ip2location import IP2LocationGatewayProtocol, IpLocation
import geoip2.database

from app.core.config import settings

class IP2LocationGateway(IP2LocationGatewayProtocol):
    
    def resolve(self, ip: str) -> IpLocation:
        
        with geoip2.database.Reader(settings.ip2location_bin_database_path) as reader:
            city = reader.city(ip)
            country = reader.country(ip)
            return IpLocation(
                city=city.city.name,
                country=country.country.name,
                country_code=country.country.iso_code,
            )