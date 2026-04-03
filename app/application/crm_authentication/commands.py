from app.application.base import FlexibleCommand


class UserLoginCommand(FlexibleCommand):
    user_login: str
    password: str
    
class UserRegistrationCommand(FlexibleCommand):
    user_login: str
    password: str
    user_name: str
    timezone: str
    ip: str | None = None
    
    
    