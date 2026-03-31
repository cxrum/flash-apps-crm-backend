from datetime import datetime

from app.application.base import BaseResponse, JsonDict


class PostbackResponseEntry(BaseResponse):
    postback_id: int
    platform_app_id: int
    name: str
    endpoint_url: str
    trigger_type: str
    http_method: str 
    headers: JsonDict
    auth_params: JsonDict
    template: JsonDict
    retry_policy: JsonDict
    timeout: int = 0
    is_active: bool = True
    event_key: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    
    
class ListPostbackResponse(BaseResponse):
    postbacks: list[PostbackResponseEntry]
    
    
class GetPostbackResponse(BaseResponse):
    postback: PostbackResponseEntry
    
    
class CreatePostbackResponse(BaseResponse):
    postback: PostbackResponseEntry
    
    
class DeletePostbackResponse(BaseResponse):
    postback: PostbackResponseEntry