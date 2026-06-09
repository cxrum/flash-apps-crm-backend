from app.application.crm_authentication.commands import (
    UserLoginCommand,
    UserRegistrationCommand,
)
from app.application.crm_authentication.exceptions import (
    EmailIsExist,
    InvalidOrExpiredToken,
    InvalidPasswordOrEmail,
)
from app.application.crm_authentication.protocol import CrmAuthenticationProtocol
from app.application.crm_authentication.responses import (
    AuthenticatedCrmUserResponse,
    CrmUserInfoResponse,
    ResolvedCrmUserResponse,
    TokenResponse,
)
from app.domain.hash_protocol import HashableValue, HashProtocol
from app.domain.uow import UnitOfWorkFactoryProtocol, UnitOfWorkProtocol
from app.domain.user import CrmUserEntity


class CrmAuthentication(CrmAuthenticationProtocol):
    def __init__(
        self,
        uow_factory: UnitOfWorkFactoryProtocol,
        hash_service: HashProtocol,
    ) -> None:
        self._uow_factory = uow_factory
        self._hash_service = hash_service

    def generate_token(self, user_id: int) -> str:
        return str(user_id)

    def __resolve_user(self, uow: UnitOfWorkProtocol, *, token: str) -> ResolvedCrmUserResponse:
        self.verify_token(token)

        exist_user = uow.user_repo.get_by_id(int(token))

        if exist_user is None or exist_user.user_id is None:
            raise InvalidOrExpiredToken()

        return ResolvedCrmUserResponse(
            crm_user_id=exist_user.user_id,
        )

    def resolve_user(self, token: str) -> ResolvedCrmUserResponse:
        self.verify_token(token)

        with self._uow_factory.create() as uow:
            exist_user = self.__resolve_user(uow, token=token)

        return ResolvedCrmUserResponse(
            crm_user_id=exist_user.user_id,
        )

    def verify_token(self, token: str) -> str:
        if not token.isnumeric():
            raise InvalidOrExpiredToken()
        return token

    def token(self, token: str) -> TokenResponse:
        self.verify_token(token)

        with self._uow_factory.create() as uow:
            exist_user = uow.user_repo.get_by_id(int(token))

            if exist_user is None or exist_user.user_id is None:
                raise InvalidOrExpiredToken()

        return TokenResponse(
            access_token=self.generate_token(exist_user.user_id),
            token_type="bearer",
        )

    def login(self, command: UserLoginCommand) -> AuthenticatedCrmUserResponse:
        with self._uow_factory.create() as uow:
            exist_user = uow.user_repo.get_by_email(command.user_login)

            if exist_user is None or exist_user.user_id is None:
                raise InvalidPasswordOrEmail()

            is_password_correct = self._hash_service.compare_hash(
                raw_value=HashableValue.from_str(command.password), hash=exist_user.password_hash
            )

            if not is_password_correct:
                raise InvalidPasswordOrEmail()

        return AuthenticatedCrmUserResponse(
            crm_user_id=exist_user.user_id,
            email=exist_user.email,
            is_active=exist_user.is_active,
            full_name=exist_user.full_name,
            access_token=self.generate_token(exist_user.user_id),
            token_type="bearer",
        )

    def login_by_token(self, token: str) -> AuthenticatedCrmUserResponse:
        with self._uow_factory.create() as uow:
            exist_user = self.__resolve_user(uow, token=token)

            if exist_user is None or exist_user.crm_user_id is None:
                raise InvalidOrExpiredToken()

            exist_user = uow.user_repo.get_by_id(exist_user.crm_user_id)

            if exist_user is None or exist_user.user_id is None:
                raise InvalidPasswordOrEmail()

        return AuthenticatedCrmUserResponse(
            crm_user_id=exist_user.user_id,
            email=exist_user.email,
            is_active=exist_user.is_active,
            full_name=exist_user.full_name,
            access_token=self.generate_token(exist_user.user_id),
            token_type="bearer",
        )

    def register(self, command: UserRegistrationCommand) -> AuthenticatedCrmUserResponse:
        with self._uow_factory.create() as uow:
            exist_user = uow.user_repo.get_by_email(command.user_login)

            if exist_user is not None:
                raise EmailIsExist()

            password = self._hash_service.hash_value(HashableValue.from_str(command.password))

            entity = CrmUserEntity(
                full_name=command.user_name,
                email=command.user_login,
                password_hash=password,
                time_zone=command.timezone,
            )

            new_crm_user = uow.user_repo.insert(entity)
        login_user = self.login(
            UserLoginCommand(
                user_login=new_crm_user.email,
                password=command.password,
            )
        )

        return login_user
