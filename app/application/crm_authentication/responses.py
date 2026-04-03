from app.application.base import BaseResponse

class ResolvedCrmUserResponse(BaseResponse):
    crm_user_id: int
    access_token: str
    token_type: str
