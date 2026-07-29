from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.modules.crm.application.admin.crm_authorization.protocol import CrmAuthorizationServiceProtocol
from app.modules.crm.application.crm_authentication.protocol import CrmAuthenticationProtocol
from app.modules.crm.application.crm_authentication.responses import ResolvedCrmUserResponse
from app.modules.crm.application.crm_authentication.service import CrmAuthentication
from app.modules.crm.di.infra import get_uow_factory
from app.modules.crm.di.services import get_crm_authorization_service, get_hash_service
from app.modules.crm.domain.hash_protocol import HashProtocol
from app.modules.crm.domain.permission.CrmPermissionEntity import CrmPermissionEntity
from app.modules.crm.domain.uow import UnitOfWorkFactoryProtocol

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@lru_cache
def stub_user_resolver(
    uow_factory: Annotated[UnitOfWorkFactoryProtocol, Depends(get_uow_factory)],
    hash_service: Annotated[HashProtocol, Depends(get_hash_service)],
) -> CrmAuthenticationProtocol:
    return CrmAuthentication(uow_factory, hash_service)


def verify_token(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_resolver: Annotated[CrmAuthenticationProtocol, Depends(stub_user_resolver)],
) -> str:
    return user_resolver.verify_token(token)


def resolve_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_resolver: Annotated[CrmAuthenticationProtocol, Depends(stub_user_resolver)],
) -> ResolvedCrmUserResponse:
    return user_resolver.resolve_user(token)


def resolve_raw_logs_user(
    app_id: int,
    crm_user: Annotated[ResolvedCrmUserResponse, Depends(resolve_user)],
    authorization_service: Annotated[CrmAuthorizationServiceProtocol, Depends(get_crm_authorization_service)],
    uow_factory: Annotated[UnitOfWorkFactoryProtocol, Depends(get_uow_factory)],
) -> ResolvedCrmUserResponse:
    with uow_factory.create() as uow:
        authorization_service.required_user_permission(
            uow=uow,
            crm_user_id=crm_user.crm_user_id,
            app_id=app_id,
            permission_code=CrmPermissionEntity.view_raw_logs_permission(),
        )
    return crm_user
