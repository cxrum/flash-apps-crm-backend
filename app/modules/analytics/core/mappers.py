from app.modules.analytics.model.models import ClickModel, CurrentParamModel, EventModel
from app.modules.analytics.types.currentParam import CurrentParam
from app.modules.analytics.types.event import Event
from app.modules.crm.infra.db.attribution.models import Click


class EventMapper:
    @classmethod
    def transport_to_domain(cls):
        pass

    @classmethod
    def row_to_domain(cls, row: EventModel) -> Event:
        return Event(
            event_id=row.event_id,
            click_id=row.click_id,
            app_user_id=row.app_user_id,
            event_type=row.event_type,
            event_key=row.event_key,
            amount=row.amount,
            currency=row.currency,
            amount_usd=row.amount_usd,
            event_time_utc=row.event_time_utc,
            payload=dict(row.payload),
            created_at=row.created_at,
        )

    @classmethod
    def domain_to_row(cls, entity: Event) -> EventModel:
        kwargs: dict[str, object] = {
            "event_id": entity.event_id,
            "click_id": entity.click_id,
            "app_user_id": entity.app_user_id,
            "event_type": entity.event_type,
            "event_key": entity.event_key,
            "amount": entity.amount,
            "currency": entity.currency,
            "amount_usd": entity.amount_usd,
            "event_time_utc": entity.event_time_utc,
            "payload": dict(entity.payload),
        }
        if entity.created_at is not None:
            kwargs["created_at"] = entity.created_at
        return EventModel(**kwargs)


class ClickMappers:
    @classmethod
    def transport_to_domain(cls):
        pass

    @classmethod
    def row_to_domain(cls, row: ClickModel) -> Click:
        return Click(
            click_id=row.click_id,
            app_platform_id=row.app_platform_id,
            status=row.status,
            raw_query=dict(row.raw_query),
            ip_address=row.ip_address,
            user_agent=row.user_agent,
            city=row.city,
            country_code=row.country_code,
            region=row.region,
            language=row.language,
            referrer=row.referrer,
            source=row.source,
            redirect_target=row.redirect_target,
            normalized_params=dict(row.normalized_params),
            created_at=row.created_at,
        )

    @classmethod
    def domain_to_row(cls, entity: Click) -> ClickModel:
        kwargs: dict[str, object] = {
            "click_id": entity.click_id,
            "app_platform_id": entity.app_platform_id,
            "status": entity.status,
            "raw_query": dict(entity.raw_query),
            "ip_address": entity.ip_address,
            "user_agent": entity.user_agent,
            "city": entity.city,
            "country_code": entity.country_code,
            "region": entity.region,
            "language": entity.language,
            "referrer": entity.referrer,
            "source": entity.source,
            "redirect_target": entity.redirect_target,
            "normalized_params": dict(entity.normalized_params),
        }
        if entity.created_at is not None:
            kwargs["created_at"] = entity.created_at
        return ClickModel(**kwargs)


class CurrentParamMappers:
    @classmethod
    def transport_to_domain(cls):
        pass

    @classmethod
    def row_to_domain(cls, row: CurrentParamModel) -> CurrentParam:
        return CurrentParam(
            click_id=row.click_id,
            param_key=row.param_key,
            value_string=row.value_string,
            value_number=row.value_number,
            value_bool=row.value_bool,
            value_json=row.value_json,
            updated_at=row.updated_at,
        )

    @classmethod
    def domain_to_row(cls, entity: CurrentParam) -> CurrentParamModel:
        kwargs: dict[str, object] = {
            "click_id": entity.click_id,
            "param_key": entity.param_key,
            "value_string": entity.value_string,
            "value_number": entity.value_number,
            "value_bool": entity.value_bool,
            "value_json": entity.value_json,
        }
        if entity.updated_at is not None:
            kwargs["updated_at"] = entity.updated_at
        return CurrentParamModel(**kwargs)
