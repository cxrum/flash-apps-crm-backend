from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.application.crm_authentication.protocol import CrmAuthenticationProtocol
from app.di.dependencies import stub_user_resolver


router = APIRouter()

@router.post("/token", tags=["authentication"])
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    authentication_service: CrmAuthenticationProtocol = Depends(stub_user_resolver)
):
    resolved_user = authentication_service.login_user(user_name=form_data.username,  password=form_data.password)
    return {"access_token": resolved_user.crm_user_id, "token_type": "bearer"}
