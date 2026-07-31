from typing import Mapping

from app.core.utils.general_mapper import GeneralMapper
from app.modules.crm.application.admin.crm_authorization.commands import (
    CreateRoleCommand,
    DeleteAppAccessCommand,
    ListRolesCommand,
    ListUsersWithAccessCommand,
    ShareAppAccessCommand,
)
from app.modules.crm.application.admin.crm_authorization.responses import (
    CrmUserResponseValue,
    PermissionResponseValue,
    RoleResponseValue,
)
from app.modules.crm.domain.permission.CrmPermissionEntity import CrmPermissionEntity
from app.modules.crm.domain.role.CrmRoleEntity import CrmRoleEntity
from app.modules.crm.domain.user.CrmUserEntity import CrmUserEntity


class AuthenticationResponseMapper:
    @classmethod
    def list_roles_from_transport(cls, payload: Mapping[str, object]) -> ListRolesCommand:
        return GeneralMapper.command_payload_to_command(ListRolesCommand, payload)

    @classmethod
    def create_role_from_transport(cls, payload: Mapping[str, object]) -> CreateRoleCommand:
        return GeneralMapper.command_payload_to_command(CreateRoleCommand, payload)

    @classmethod
    def share_app_access_from_transport(cls, payload: Mapping[str, object]) -> ShareAppAccessCommand:
        return GeneralMapper.command_payload_to_command(ShareAppAccessCommand, payload)

    @classmethod
    def list_users_with_access_from_transport(
        cls,
        payload: Mapping[str, object],
    ) -> ListUsersWithAccessCommand:
        return GeneralMapper.command_payload_to_command(ListUsersWithAccessCommand, payload)

    @classmethod
    def delete_app_access_from_transport(cls, payload: Mapping[str, object]) -> DeleteAppAccessCommand:
        return GeneralMapper.command_payload_to_command(DeleteAppAccessCommand, payload)


class AuthenticationCommandsMapper:
    @classmethod
    def permission_domain_to_value(cls, domain: CrmPermissionEntity) -> PermissionResponseValue:
        return PermissionResponseValue.model_validate(domain)

    @classmethod
    def role_domain_to_value(cls, domain: CrmRoleEntity) -> RoleResponseValue:
        return RoleResponseValue(
            role_id=domain.role_id,
            key=domain.code,
            name=domain.display_name,
        )

    @classmethod
    def user_domain_to_value(cls, domain: tuple[CrmUserEntity, CrmRoleEntity]) -> CrmUserResponseValue:
        return CrmUserResponseValue(
            full_name=domain[0].full_name,
            email=domain[0].email,
            role=domain[1].display_name,
            is_active=domain[0].is_active,
            crm_user_id=domain[0].user_id,
            created_at=domain[0].created_at,
            updated_at=domain[0].updated_at,
        )
