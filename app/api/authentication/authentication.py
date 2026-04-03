from typing import Annotated

from fastapi import APIRouter, Body, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm

from app.api.authentication.payloads import UserRegistrationSchemaPayload
from app.application.base import JsonDict
from app.application.crm_authentication.commands import UserLoginCommand, UserRegistrationCommand
from app.application.crm_authentication.protocol import CrmAuthenticationProtocol
from app.di.dependencies import stub_user_resolver


router = APIRouter()

@router.post("/token", tags=["authentication"])
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    authentication_service: CrmAuthenticationProtocol = Depends(stub_user_resolver)
) -> JsonDict:
    resolved_user = authentication_service.login(
        UserLoginCommand(
            user_login=form_data.username, 
            password=form_data.password
        )
    )
    return resolved_user.model_dump()

@router.post("/register", tags=["authentication"])
def register(
    request: Request,
    body: Annotated[UserRegistrationSchemaPayload, Body()],
    authentication_service: CrmAuthenticationProtocol = Depends(stub_user_resolver),
) -> JsonDict:
    resolved_user = authentication_service.register(
        UserRegistrationCommand(
            user_login=body.login,
            password=body.password,
            user_name=body.full_name,
            ip=request.client.host if request.client is not None else None,
            timezone=body.timezone
        )
    )
    
    return resolved_user.model_dump()
