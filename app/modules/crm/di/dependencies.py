from functools import lru_cache

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.modules.crm.application.crm_authentication.protocol import CrmAuthenticationProtocol
from app.modules.crm.application.crm_authentication.responses import ResolvedCrmUserResponse
from app.modules.crm.application.crm_authentication.service import CrmAuthentication
from app.modules.crm.di.infra import get_uow_factory
from app.modules.crm.di.services import get_hash_service
from app.modules.crm.domain.hash_protocol import HashProtocol
from app.modules.crm.domain.uow import UnitOfWorkFactoryProtocol


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@lru_cache
def stub_user_resolver(
    uow_factory: UnitOfWorkFactoryProtocol = Depends(get_uow_factory),
    hash_service: HashProtocol = Depends(get_hash_service),
) -> CrmAuthenticationProtocol:
    return CrmAuthentication(uow_factory, hash_service)


def verify_token(
    token: str = Depends(oauth2_scheme), user_resolver: CrmAuthenticationProtocol = Depends(stub_user_resolver)
) -> str:
    return user_resolver.verify_token(token)


def resolve_user(
    token: str = Depends(oauth2_scheme), user_resolver: CrmAuthenticationProtocol = Depends(stub_user_resolver)
) -> ResolvedCrmUserResponse:
    return user_resolver.resolve_user(token)
