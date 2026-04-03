from typing import Mapping

from app.application.admin.crm_authorization.commands import CreateRoleCommand, DeleteAppAccessCommand, ListRolesCommand, ListUsersWithAccessCommand, ShareAppAccessCommand
from app.application.admin.crm_authorization.responses import CrmUserResponseValue, RoleResponseValue, PermissionResponseValue
from app.core.utils.general_mapper import GeneralMapper
from app.domain.permission.CrmPermissionEntity import CrmPermissionEntity
from app.domain.role.CrmRoleEntity import CrmRoleEntity
from app.domain.user import CrmUserEntity


class CrmUserResponseMapper:
    pass
    
class CrmCommandsMapper:
    pass