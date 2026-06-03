from app.application.base import BaseResponse

class ResolvedCrmUserResponse(BaseResponse):
    crm_user_id: int
    full_name: str
    email: str
    is_active: bool = True
    access_token: str
    token_type: str
