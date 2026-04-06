from typing import Any, Dict

from app.application.admin.exception import AdminException


class DefinitionsExceptions(AdminException):
    def __init__(self, message_key: str = "internal", context: Dict[str, Any]={}, code: int = 500):
        super().__init__(message_key, context, code)

class MetricDefinitionNotFound(DefinitionsExceptions):
    def __init__(self, metric_definition_id: int | None = None):
        context = {"metric_definition_id": metric_definition_id} if metric_definition_id is not None else {}
        super().__init__("admin.definition.metric.not_found", context, 404)
        
class ConversionDefinitionNotFound(DefinitionsExceptions):
    def __init__(self, conversion_definition_id: int | None = None):
        context = {"conversion_definition_id": conversion_definition_id} if conversion_definition_id is not None else {}
        super().__init__("admin.definition.conversion.not_found", context, 404)
        
class ParamDefinitionNotFound(DefinitionsExceptions):
    def __init__(self, param_definition_id: int | None = None):
        context = {"param_definition_id": param_definition_id} if param_definition_id is not None else {}
        super().__init__("admin.definition.param.not_found", context, 404)


class DefinitionAppMismatch(DefinitionsExceptions):
    def __init__(self, definition_type: str, app_id: int):
        super().__init__(
            "admin.definition.app.mismatch",
            {"definition_type": definition_type, "app_id": app_id},
            404,
        )
