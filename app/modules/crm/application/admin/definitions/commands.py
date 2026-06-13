from app.modules.crm.application.base import FlexibleCommand, PaginationCommand


class UpdateParamDefinitionCommand(FlexibleCommand):
    crm_user_id: int
    app_id: int
    param_definition_id: int
    key: str | None = None
    name: str | None = None
    data_type: str | None = None
    description: str | None = None
    overwrite_policy: str | None = None
    is_active: bool | None = None
    visible_in_logs: bool | None = None
    visible_in_stats: bool | None = None
    filterable: bool | None = None
    groupable: bool | None = None


class ListMetricDefinitionsCommand(PaginationCommand):
    crm_user_id: int
    app_id: int


class GetMetricDefinitionCommand(FlexibleCommand):
    crm_user_id: int
    app_id: int
    metric_definition_id: int


class UpdateMetricDefinitionCommand(FlexibleCommand):
    crm_user_id: int
    app_id: int
    metric_definition_id: int
    key: str | None = None
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


class DeleteMetricDefinitionCommand(FlexibleCommand):
    crm_user_id: int
    app_id: int
    metric_definition_id: int


class ListConversionDefinitionsCommand(PaginationCommand):
    crm_user_id: int
    app_id: int


class GetConversionDefinitionCommand(FlexibleCommand):
    crm_user_id: int
    app_id: int
    conversion_definition_id: int


class CreateConversionDefinitionCommand(FlexibleCommand):
    crm_user_id: int
    app_id: int
    key: str
    name: str
    description: str | None = None
    revenue_enabled: bool = True
    expects_amount: bool = True
    expects_currency: bool = True
    dedup_mode: str | None = None
    is_active: bool = True


class UpdateConversionDefinitionCommand(FlexibleCommand):
    crm_user_id: int
    app_id: int
    conversion_definition_id: int
    key: str | None = None
    name: str | None = None
    description: str | None = None
    revenue_enabled: bool | None = None
    expects_amount: bool | None = None
    expects_currency: bool | None = None
    dedup_mode: str | None = None


class DeleteConversionDefinitionCommand(FlexibleCommand):
    crm_user_id: int
    app_id: int
    conversion_definition_id: int


class ListParamDefinitionsCommand(PaginationCommand):
    crm_user_id: int
    app_id: int


class GetParamDefinitionCommand(FlexibleCommand):
    crm_user_id: int
    app_id: int
    param_definition_id: int


class DeleteParamDefinitionCommand(FlexibleCommand):
    crm_user_id: int
    app_id: int
    param_definition_id: int


class CreateParamDefinitionCommand(FlexibleCommand):
    crm_user_id: int
    app_id: int
    key: str
    label: str
    param_type: str
    description: str | None = None
    overwrite_policy: str | None = None
    is_active: bool | None = None
    visible_in_logs: bool | None = None
    visible_in_stats: bool | None = None
    filterable: bool | None = None
    groupable: bool | None = None
    is_required: bool = False


class CreateMetricDefinitionCommand(FlexibleCommand):
    crm_user_id: int
    app_id: int
    key: str
    name: str
    description: str | None = None
    is_active: bool = True
