from collections.abc import Iterator

from fastapi import Depends

from app.application.sdk.usecases.apps.CreateAppUseCase import CreateAppUseCase
from app.application.sdk.usecases.apps.CreatePlatformUseCase import CreatePlatformUseCase
from app.application.sdk.usecases.apps.app_config import AppConfigUseCases
from app.domain.uow import CrmUnitOfWorkProtocol
from app.infra.db.puow import SqlAlchemyUnitOfWork
from app.infra.db.session import SessionLocal


def get_uow() -> Iterator[CrmUnitOfWorkProtocol]:
    with SqlAlchemyUnitOfWork(SessionLocal) as uow:
        yield uow


def get_sdk_create_app_usecase(
    uow: CrmUnitOfWorkProtocol = Depends(get_uow),
) -> CreateAppUseCase:
    return CreateAppUseCase(uow)


def get_sdk_create_platform_usecase(
    uow: CrmUnitOfWorkProtocol = Depends(get_uow),
) -> CreatePlatformUseCase:
    return CreatePlatformUseCase(uow)


def get_sdk_app_config_usecase(
    uow: CrmUnitOfWorkProtocol = Depends(get_uow),
) -> AppConfigUseCases:
    return AppConfigUseCases(uow)
