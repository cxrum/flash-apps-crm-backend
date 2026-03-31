from app.application.crm_authentication.entities import ResolvedCrmUser


from typing import Protocol


class CrmAuthenticationProtocol(Protocol):

    def verify_token(self, token: str) -> str: ...
    def resolve_user(self, token: str) -> ResolvedCrmUser: ...
    def login_user(self, user_name: str, password: str) -> ResolvedCrmUser: ...