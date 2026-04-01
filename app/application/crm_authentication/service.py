
from app.application.crm_authentication.protocol import CrmAuthenticationProtocol
from app.application.crm_authentication.entities import ResolvedCrmUser

class StubCrmAuthentication(CrmAuthenticationProtocol):
    
    def resolve_user(self, token: str) -> ResolvedCrmUser:
        self.verify_token(token)
        
        return ResolvedCrmUser(
            crm_user_id=int(token),
            time_zone="UTC"
        )
        
    def verify_token(self, token: str) -> str: 
        if not token.isnumeric():
            raise Exception()
        return token
        
    def login_user(self, user_name: str, password: str) -> ResolvedCrmUser:
        if not user_name.isnumeric():
            raise Exception("Incorrect username or password")
        
        return ResolvedCrmUser(
            crm_user_id=int(user_name),
            time_zone="UTC"
        )