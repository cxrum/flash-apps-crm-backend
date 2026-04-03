from collections.abc import Mapping
from copy import deepcopy
from dataclasses import asdict
from typing import Any, TypeVar

from pydantic import BaseModel

from app.application.crm_authentication.responses import ResolvedCrmUserResponse
from app.domain.pagination import Pagination

TCommand = TypeVar("TCommand", bound=BaseModel)
TDomainEntity = TypeVar("TDomainEntity", bound=BaseModel)
TResponseValue = TypeVar("TResponseValue", bound=BaseModel)

class GeneralMapper:

    @staticmethod
    def to_dict(*payloads: BaseModel, **extra: object) -> dict[str, Any]:
        data: dict[str, Any] = {}
        for payload in payloads:
            data.update(payload.model_dump(exclude_none=True))
        data.update({key: value for key, value in extra.items() if value is not None})
        return data
    
    @staticmethod
    def transport_to_command_payload(
        crm_user: ResolvedCrmUserResponse,
        *payloads: BaseModel,
        **extra: object,
    ) -> dict[str, Any]:
        return GeneralMapper.to_dict(*payloads, crm_user_id=crm_user.crm_user_id, **extra)
    
    @staticmethod
    def command_payload_to_command(command_type: type[TCommand], payload: Mapping[str, object]) -> TCommand:
        return command_type.model_validate(dict(payload))

    @staticmethod
    def domain_to_response_value(
        response_value_type: type[TResponseValue], 
        domain_payload: Mapping[str, object],  
        **extra: object
    ) -> TResponseValue:
        _domain_payload: dict[str, Any] = deepcopy(dict(domain_payload))
        _domain_payload.update({key: value for key, value in extra.items() if value is not None})
        return response_value_type.model_validate(_domain_payload)
