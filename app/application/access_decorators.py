from __future__ import annotations

import inspect
from functools import wraps
from typing import Any, Callable, Protocol

from app.application.admin.crm_authorization.protocol import CrmAuthorizationServiceProtocol
from app.application.exception import AppNotFound, UserNotFound
from app.domain.role.CrmRoleEntity import Roles
from app.domain.uow import UnitOfWorkFactoryProtocol, UnitOfWorkProtocol


class AuthorizationAwareService(Protocol):
    _authorization_service: CrmAuthorizationServiceProtocol
    _uow_factory: UnitOfWorkFactoryProtocol


AccessContextResolver = Callable[
    [AuthorizationAwareService, UnitOfWorkProtocol, Any],
    tuple[int | None, int | None],
]


def _resolve_command(bound_arguments: inspect.BoundArguments) -> Any:
    command = bound_arguments.arguments.get("command")
    if command is not None:
        return command

    for name, value in bound_arguments.arguments.items():
        if name == "self":
            continue
        if hasattr(value, "crm_user_id") and hasattr(value, "app_id"):
            return value

    return None


def _access_decorator(
    required_role: Roles | None = None,
    required_permission: str | None = None,
    context_resolver: AccessContextResolver | None = None,
):
    def decorator(func):
        signature = inspect.signature(func)

        @wraps(func)
        def wrapper(self: AuthorizationAwareService, *args, **kwargs):
            bound_arguments = signature.bind_partial(self, *args, **kwargs)
            bound_arguments.apply_defaults()

            command = _resolve_command(bound_arguments)
            crm_user_id = getattr(command, "crm_user_id", None)
            app_id = getattr(command, "app_id", None)

            with self._uow_factory.create() as uow:
                if context_resolver is not None:
                    resolved_user_id, resolved_app_id = context_resolver(
                        self,
                        uow,
                        command,
                    )
                    if crm_user_id is None:
                        crm_user_id = resolved_user_id
                    if app_id is None:
                        app_id = resolved_app_id

                if crm_user_id is None:
                    raise UserNotFound()
                if app_id is None:
                    raise AppNotFound()

                _authorize_access(
                    self._authorization_service,
                    uow,
                    crm_user_id=crm_user_id,
                    app_id=app_id,
                    required_role=required_role,
                    required_permission=required_permission,
                )

            return func(self, *args, **kwargs)

        return wrapper

    return decorator


def _authorize_access(
    authorization_service: CrmAuthorizationServiceProtocol,
    uow: UnitOfWorkProtocol,
    *,
    crm_user_id: int,
    app_id: int,
    required_role: Roles | None,
    required_permission: str | None,
) -> Any:
    if required_permission is not None:
        return authorization_service.required_user_permission(
            uow=uow,
            crm_user_id=crm_user_id,
            app_id=app_id,
            permission_code=required_permission,
        )

    if required_role is None:
        return authorization_service.get_user_role(
            uow=uow,
            crm_user_id=crm_user_id,
            app_id=app_id,
        )

    return authorization_service.required_user_role(
        uow=uow,
        crm_user_id=crm_user_id,
        app_id=app_id,
        level=required_role,
    )


def require_app_access(context_resolver: AccessContextResolver | None = None):
    return _access_decorator(context_resolver=context_resolver)


def require_role(role: Roles, context_resolver: AccessContextResolver | None = None):
    return _access_decorator(required_role=role, context_resolver=context_resolver)


def require_permission(
    permission_code: str,
    context_resolver: AccessContextResolver | None = None,
):
    return _access_decorator(
        required_permission=permission_code,
        context_resolver=context_resolver,
    )
