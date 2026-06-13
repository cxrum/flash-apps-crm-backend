from dataclasses import dataclass
from datetime import datetime


@dataclass()
class CrmPermissionEntity:
    code: str
    description: str | None = None
    permission_id: int | None = None
    created_at: datetime | None = None
    
    @classmethod
    def permission_list(cls) -> dict[str, str]:
        """
        Returns { code: description } 
        """

        return {
            cls.view_stats_permission(): "",
            cls.view_raw_logs_permission(): "",
            cls.manage_push_permission(): "",
            cls.edit_app_config_permission(): "",
            cls.export_data_permission(): ""
        }
    
    @staticmethod 
    def view_stats_permission() -> str: return "view_stats"
    
    @staticmethod 
    def view_raw_logs_permission() -> str: return "view_raw_logs"
    
    @staticmethod 
    def manage_push_permission() -> str: return "manage_push"
    
    @staticmethod 
    def edit_app_config_permission() -> str: return "edit_app_config"
    
    @staticmethod 
    def export_data_permission() -> str: return "export_data"