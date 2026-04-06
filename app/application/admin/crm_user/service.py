from dataclasses import dataclass

from app.application.admin.crm_authorization.commands import GrantUserAppAccess, GrantUserAppPermission, ListPermissionCommand, ListAppUsersCommand, ListUserPermissionCommand, RemoveUserAppAccess, RemoveUserAppPermission
from app.application.admin.crm_authorization.mappers import AuthenticationCommandsMapper
from app.application.admin.crm_authorization.responses import GrantUserAppAccessResponse, GrantUserPermissionResponse, ListAppUsersResponse, ListPermissionsResponse, ListUserPermissionResponse, RemoveUserAppAccessResponse, RemoveUserPermissionResponse
from app.application.exception import GeneralException
from app.application.mapper import PaginationMapper
from app.core.utils.general_mapper import GeneralMapper
from app.domain.permission.CrmPermissionEntity import CrmPermissionEntity
from app.domain.role.CrmRoleEntity import CrmRoleEntity
from app.domain.uow import UnitOfWorkFactoryProtocol, UnitOfWorkProtocol
from app.domain.user import CrmUserEntity
from app.domain.user_app_access.CrmUserAppAccessEntity import CrmUserAppAccessEntity
from app.domain.user_permissions.CrmUserPermissionEntity import CrmUserPermissionEntity

    

class CrmUserService:
    def __init__(
        self,
        uow_factory: UnitOfWorkFactoryProtocol,
    ) -> None:
        self._uow_factory = uow_factory
    
    