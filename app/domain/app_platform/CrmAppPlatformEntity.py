from dataclasses import dataclass
from datetime import datetime


@dataclass()
class CrmAppPlatformEntity:
    app_id: int
    platform: str
    package_name: str
    install_key: str
    store_url: str | None = None
    sdk_public_key: str | None = None
    sdk_secret_hash: str | None = None
    status: str = "active"
    platform_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    
    @staticmethod
    def __aviable_statuses() -> list[str]:
        return ['active', 'inactive'] 
    
    @staticmethod
    def __aviable_platforms() -> list[str]:
        return ['android', 'ios']
    
    def is_valid_platform(self)->bool:
        return self.platform in CrmAppPlatformEntity.__aviable_platforms()
    
    def is_valid_status(self)->bool:
        return self.status in CrmAppPlatformEntity.__aviable_statuses()
    
    def activate(self):
        self.status = "active"
        self.updated_at = datetime.now()
        
    def deactivate(self):
        self.status = "inactive"
        self.updated_at = datetime.now()