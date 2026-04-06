
from datetime import UTC, date, datetime
import json
from typing import Any

from app.application.exception import GeneralException
from app.domain.app_platform.CrmAppPlatformEntity import CrmAppPlatformEntity
from app.domain.currency.entity import Money
from app.domain.custom_params_statistics_aggregate.CustomParamsStatisticsAggregateEntity import CustomParamsStatisticsAggregateEntity
from app.domain.event_bus.events.crm_events import RawEventMessage
from app.domain.param_definition.CrmParamDefinitionEntity import CrmParamDefinitionEntity, DefaultParamKeys
from app.domain.statistics_aggregate import StatisticsAggregateEntity
from app.domain.uow import UnitOfWorkProtocol


class StatisticAggregates:
        
    @staticmethod
    def _serialize_param_value(value: Any) -> str:
        if isinstance(value, datetime):
            return value.isoformat()
        if isinstance(value, date):
            return value.isoformat()
        if isinstance(value, tuple | set):
            return json.dumps(list(value), default=str, sort_keys=True)
        if isinstance(value, list | dict):
            return json.dumps(value, default=str, sort_keys=True)
        return str(value)
    
    @staticmethod
    def update(*, uow: UnitOfWorkProtocol, message: RawEventMessage, revenue_enabled: bool, app_platform: CrmAppPlatformEntity):
        if app_platform.platform_id is None:
            raise GeneralException()
        
        definitions = uow.param_definition_repo.list_by_app_id(app_platform.app_id)
        
        filtered_payload = CrmParamDefinitionEntity.get_params_for_aggregation(
            params=message.raw_payload,
            params_dictionary=definitions,
        )
        
        geo = filtered_payload[DefaultParamKeys.GEO.value]
        
        current_conversion_statistic = uow.statistics_repo.list_by_filters(
            event_type=message.event_type,
            event_key=message.event_key,
            ddate=datetime.now(UTC).date(),
            geo = geo
        ) 
        
        if len(current_conversion_statistic) > 1:
            raise GeneralException( )
        
        if len(current_conversion_statistic) == 0:
            current_conversion_statistic.append(
                uow.statistics_repo.save(StatisticsAggregateEntity(
                        app_platform_id=app_platform.platform_id,
                        geo=geo,
                        ddate=datetime.now(UTC).date(),
                        event_type=message.event_type,
                        event_key=message.event_key,
                        count=0
                    )
                )
            )
        
        for conversion in current_conversion_statistic:
            conversion.increase_count()
            if revenue_enabled and message.amount_usd is not None:
                conversion.increase_amount_usd(Money(
                    "USD",
                    message.amount_usd
                ))
            
        uow.statistics_repo.save_many(
            current_conversion_statistic
        )
        
        for param_key, param_value in filtered_payload.items():
            serialized_param_value = StatisticAggregates._serialize_param_value(param_value)
            current_conversion_detailed_statistic = uow.custom_params_statistics_repo.list_by_filters(
                event_type=message.event_type,
                event_key=message.event_key,
                param_key=param_key,
                param_value=serialized_param_value,
                ddate=datetime.now(UTC).date(),
                geo=geo,
            )
            
            if len(current_conversion_detailed_statistic) > 1:
                raise GeneralException( )
            
            if len(current_conversion_detailed_statistic) == 0:
                current_conversion_detailed_statistic.append(
                    uow.custom_params_statistics_repo.save(CustomParamsStatisticsAggregateEntity(
                            app_platform_id=app_platform.platform_id,
                            geo=geo,
                            ddate=datetime.now(UTC).date(),
                            event_type=message.event_type,
                            event_key=message.event_key,
                            param_key=param_key,
                            param_value=serialized_param_value,
                            count=0
                        )
                    )
                )
                
            for conversion in current_conversion_detailed_statistic:
                conversion.increase_count()
                if revenue_enabled and message.amount_usd is not None:
                    conversion.increase_amount_usd(Money(
                        "USD",
                        message.amount_usd
                    ))
                
            uow.custom_params_statistics_repo.save_many(
                current_conversion_detailed_statistic
            )
            