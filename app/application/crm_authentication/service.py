
from app.application.contracts.ip2location import IP2LocationGatewayProtocol
from app.application.crm_authentication.commands import UserLoginCommand, UserRegistrationCommand
from app.application.crm_authentication.exceptions import EmailIsExist, InvalidOrExpiredToken, InvalidPasswordOrEmail
from app.application.crm_authentication.protocol import CrmAuthenticationProtocol
from app.application.crm_authentication.responses import ResolvedCrmUserResponse
from app.application.exception import GeneralException
from app.domain.hash_protocol import HashProtocol, HashableValue
from app.domain.uow import UnitOfWorkFactoryProtocol
from app.domain.user import CrmUserEntity

class CrmAuthentication(CrmAuthenticationProtocol):

    def __init__(
        self,
        uow_factory: UnitOfWorkFactoryProtocol,
        hash_service: HashProtocol,
    ) -> None:
        self._uow_factory = uow_factory
        self._hash_service= hash_service
        
    def resolve_user(self, token: str) -> ResolvedCrmUserResponse:
        self.verify_token(token)

        with self._uow_factory.create() as uow:
            exist_user = uow.user_repo.get_by_id(int(token))
            
            if exist_user is None or exist_user.user_id is None:
                raise InvalidOrExpiredToken()
        
        return ResolvedCrmUserResponse(
            crm_user_id=exist_user.user_id,
            access_token=str(exist_user.user_id),
            token_type="bearer",
        )
        
    def verify_token(self, token: str) -> str: 
        if not token.isnumeric():
            raise Exception()
        return token
    
    def login(self, command: UserLoginCommand) -> ResolvedCrmUserResponse:
        with self._uow_factory.create() as uow:
            exist_user = uow.user_repo.get_by_email(command.user_login)
            
            if exist_user is None or exist_user.user_id is None:
                raise InvalidPasswordOrEmail()
            
            is_password_correct = self._hash_service.compare_hash(
                raw_value=HashableValue.from_str(command.password),
                hash=exist_user.password_hash
            )
            
            if not is_password_correct:
                raise InvalidPasswordOrEmail()
            
        return ResolvedCrmUserResponse(
            crm_user_id=exist_user.user_id,
            access_token=str(exist_user.user_id),
            token_type="bearer"
        )
    
    def register(self, command: UserRegistrationCommand) -> ResolvedCrmUserResponse:
        with self._uow_factory.create() as uow:
            exist_user = uow.user_repo.get_by_email(command.user_login)
            
            if exist_user is not None:
                raise EmailIsExist()
            
            password = self._hash_service.hash_value(
                HashableValue.from_str(command.password)
            )
            
            entity = CrmUserEntity(
                full_name=command.user_name,
                email=command.user_login,
                password_hash=password,
                time_zone=command.timezone
            )
            
            new_crm_user = uow.user_repo.insert(
                entity
            )
        
        login_user = self.login(UserLoginCommand(
            user_login=new_crm_user.email,
            password=command.password,
        ))
                    
        return login_user