from typing import Any, Dict

from app.domain.exceptions import DomainException


class ParamDefinitionException(DomainException):
    def __init__(self, message_key: str = "internal", context: Dict[str, Any]={}, code: int = 400):
        super().__init__(message_key, context, code)


class InvalidParamDataType(ParamDefinitionException):
    def __init__(self, data_type: str):
        super().__init__("domain.param_definition.data_type.invalid", {"data_type": data_type}, 400)


class InvalidParamValue(ParamDefinitionException):
    def __init__(self, machine_key: str, data_type: str, value: object):
        super().__init__(
            "domain.param_definition.value.invalid",
            {
                "machine_key": machine_key,
                "data_type": data_type,
                "value": value,
            },
            400,
        )
