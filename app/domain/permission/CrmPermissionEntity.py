from dataclasses import dataclass
from datetime import datetime


@dataclass()
class CrmPermissionEntity:
    code: str
    description: str | None = None
    permission_id: int | None = None
    created_at: datetime | None = None
    
    @classmethod
    def permision_list(cls) -> dict[str, str]:
        """
        Returns { code: description } 
        """

        return {
            cls.view_stats_permision(): "",
            cls.view_raw_logs_permision(): "",
            cls.manage_push_permision(): "",
            cls.edit_app_config_permision(): "",
            cls.export_data_permision(): ""
        }
    
    @staticmethod 
    def view_stats_permision() -> str: return "view_stats"
    
    @staticmethod 
    def view_raw_logs_permision() -> str: return "view_raw_logs"
    
    @staticmethod 
    def manage_push_permision() -> str: return "manage_push"
    
    @staticmethod 
    def edit_app_config_permision() -> str: return "edit_app_config"
    
    @staticmethod 
    def export_data_permision() -> str: return "export_data"