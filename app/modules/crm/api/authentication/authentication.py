from typing import Annotated

from fastapi import APIRouter, Body, Depends, Form, Header, Request

from app.modules.crm.api.authentication.payloads import UserRegistrationSchemaPayload
from app.modules.crm.application.base import JsonDict
from app.modules.crm.application.crm_authentication.commands import UserLoginCommand, UserRegistrationCommand
from app.modules.crm.application.crm_authentication.exceptions import InvalidOrExpiredToken, InvalidPasswordOrEmail
from app.modules.crm.application.crm_authentication.protocol import CrmAuthenticationProtocol
from app.modules.crm.di.dependencies import stub_user_resolver

router = APIRouter()


def _extract_bearer_token(authorization: str | None) -> str | None:
    if authorization is None:
        return None

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise InvalidOrExpiredToken()

    return token


@router.post("/token", tags=["authentication"])
def login(
    authentication_service: Annotated[CrmAuthenticationProtocol, Depends(stub_user_resolver)],
    username: Annotated[str | None, Form()] = None,
    password: Annotated[str | None, Form()] = None,
    authorization: Annotated[str | None, Header()] = None,
) -> JsonDict:
    token = _extract_bearer_token(authorization)

    if token is not None:
        resolved_user = authentication_service.login_by_token(token)
    elif username is not None and password is not None:
        resolved_user = authentication_service.login(
            UserLoginCommand(
                user_login=username,
                password=password,
            )
        )
    else:
        raise InvalidPasswordOrEmail()

    return resolved_user.model_dump()


@router.post("/register", tags=["authentication"])
def register(
    request: Request,
    body: Annotated[UserRegistrationSchemaPayload, Body()],
    authentication_service: Annotated[CrmAuthenticationProtocol, Depends(stub_user_resolver)],
) -> JsonDict:
    resolved_user = authentication_service.register(
        UserRegistrationCommand(
            user_login=body.login,
            password=body.password,
            user_name=body.full_name,
            ip=request.client.host if request.client is not None else None,
            timezone=body.timezone,
        )
    )

    return resolved_user.model_dump()
