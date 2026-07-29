from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Self

from app.modules.analytics.application.ingestion.exception import (
    BuilderEventTypeMismatch,
    EventClickIdRequired,
    EventIdRequired,
    EventKeyRequired,
    InvalidEventPayload,
    MoneyValueNegative,
    ReservedEventPayloadKeys,
    RevenueAmountRequired,
    RevenueCurrencyInvalid,
    RevenueCurrencyRequired,
)
from app.modules.analytics.application.ingestion.exception import (
    ConversionMoneyValueException,
    MetricMoneyValueException,
)
from app.modules.analytics.domain.events.AnalyticsEventEntity import AnalyticsEventEntity


class _BaseSdkEventBuilder:
    _reserved_payload_keys = frozenset(
        {
            "event_id",
            "click_id",
            "event_type",
            "event_key",
            "event_time_utc",
            "app_user_id",
            "amount",
            "currency",
            "amount_usd",
            "created_at",
        }
    )
    _event_type: str

    def __init__(
        self,
        *,
        event_id: str,
        click_id: str,
        event_key: str,
        app_user_id: int | None = None,
        event_time_utc: datetime | None = None,
        payload: dict[str, Any] | None = None,
        created_at: datetime | None = None,
    ) -> None:
        if not event_id:
            raise EventIdRequired()
        if not click_id:
            raise EventClickIdRequired()

        self._event_id = event_id
        self._click_id = click_id
        self._app_user_id = app_user_id
        self._event_key = ""
        self._amount: float | None = None
        self._currency: str | None = None
        self._amount_usd: float | None = None
        self._event_time_utc = self._coerce_datetime(event_time_utc) if event_time_utc is not None else None
        self._payload: dict[str, Any] = {}
        self._created_at = self._coerce_datetime(created_at) if created_at is not None else None

        self._set_event_type(self._event_type)
        self._set_event_key(event_key)
        if payload is not None:
            self._set_payload(payload)

    @staticmethod
    def _coerce_datetime(value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=UTC)
        return value.astimezone(UTC)

    @staticmethod
    def _coerce_amount(value: float | None) -> float | None:
        if value is None:
            return None
        if value < 0:
            raise MoneyValueNegative()
        return float(value)

    def _set_event_type(self, value: str) -> Self:
        if value != self._event_type:
            raise BuilderEventTypeMismatch(builder=self.__class__.__name__, event_type=value)
        return self

    def _set_event_key(self, value: str) -> Self:
        if not value:
            raise EventKeyRequired()
        self._event_key = value
        return self

    def _set_event_time_utc(self, value: datetime) -> Self:
        self._event_time_utc = self._coerce_datetime(value)
        return self

    def _set_payload(self, value: dict[str, Any]) -> Self:
        payload = self.form_payload(**value)
        if not self.validate_payload(payload):
            raise InvalidEventPayload()
        self._payload = payload
        return self

    def _set_created_at(self, value: datetime | None) -> Self:
        self._created_at = self._coerce_datetime(value) if value is not None else None
        return self

    def validate_payload(self, payload: dict[str, Any]) -> bool:
        return True

    def form_payload(self, **kwargs: Any) -> dict[str, Any]:
        payload = dict(kwargs)
        if not self._reserved_payload_keys.isdisjoint(payload):
            raise ReservedEventPayloadKeys()
        return payload

    def _validate_money_fields(self) -> None:
        raise NotImplementedError

    def build(self) -> AnalyticsEventEntity:
        self._validate_money_fields()
        return AnalyticsEventEntity(
            event_id=self._event_id,
            click_id=self._click_id,
            app_user_id=self._app_user_id,
            event_type=self._event_type,
            event_key=self._event_key,
            amount=self._amount,
            currency=self._currency,
            amount_usd=self._amount_usd,
            event_time_utc=self._event_time_utc or datetime.now(tz=UTC),
            payload=dict(self._payload),
            created_at=self._created_at,
        )


class MetricsEventBuilder(_BaseSdkEventBuilder):
    _event_type = "metric"

    def _set_amount(self, value: float | None) -> Self:
        if value is not None:
            raise MetricMoneyValueException()
        self._amount = None
        return self

    def _set_currency(self, value: str | None) -> Self:
        if value is not None:
            raise MetricMoneyValueException()
        self._currency = None
        return self

    def _set_amount_in_usd(self, value: float | None) -> Self:
        if value is not None:
            raise MetricMoneyValueException()
        self._amount_usd = None
        return self

    def _validate_money_fields(self) -> None:
        if self._amount is not None or self._currency is not None or self._amount_usd is not None:
            raise MetricMoneyValueException()


class RevenueEventBuilder(_BaseSdkEventBuilder):
    _event_type = "conversion"

    def _set_amount(self, value: float | None) -> Self:
        self._amount = self._coerce_amount(value)
        return self

    def _set_currency(self, value: str | None) -> Self:
        if value is None or not value.strip():
            self._currency = None
            return self
        normalized = value.strip().upper()
        if len(normalized) != 3:
            raise RevenueCurrencyInvalid()
        self._currency = normalized
        return self

    def _set_amount_in_usd(self, value: float | None) -> Self:
        self._amount_usd = self._coerce_amount(value)
        return self

    def _validate_money_fields(self) -> None:
        if self._amount is None:
            raise RevenueAmountRequired()
        if self._currency is None:
            raise RevenueCurrencyRequired()


class ConversionEventBuilder(_BaseSdkEventBuilder):
    _event_type = "conversion"

    def _set_amount(self, value: float | None) -> Self:
        if value is not None:
            raise ConversionMoneyValueException()
        self._amount = None
        return self

    def _set_currency(self, value: str | None) -> Self:
        if value is not None:
            raise ConversionMoneyValueException()
        self._currency = None
        return self

    def _set_amount_in_usd(self, value: float | None) -> Self:
        if value is not None:
            raise ConversionMoneyValueException()
        self._amount_usd = None
        return self

    def _validate_money_fields(self) -> None:
        if self._amount is not None or self._currency is not None or self._amount_usd is not None:
            raise ConversionMoneyValueException()
