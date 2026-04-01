from app.application.base import BaseResponse

class CrmUserTokenResponse(BaseResponse):
    token: str

class ResolvedCrmUser(BaseResponse):
    crm_user_id: int
    time_zone: str