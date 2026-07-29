from typing import Any, Dict


class AnalyticsMessageResolver:
    CATALOG: dict[str, str] = {
        "internal": "Internal server error",
        "general.platform.not_found": "Platform doesn't exist",
        "sdk.click.not_found": "Click '{click_id}' does not exist",
        "sdk.ingestion.install_key.invalid": "Install key '{install_key}' is invalid",
        "sdk.idempotency.processing": "Request with idempotency key '{idempotency_key}' is still processing",
        "sdk.idempotency.state_lost": "Idempotency state for key '{idempotency_key}' was lost",
        "sdk.ingestion.event.type.unsupported": "Unsupported event type: {event_type}",
        "sdk.ingestion.revenue.data.required": "Revenue events require both amount and currency",
        "sdk.event.id.required": "Event id is required",
        "sdk.click.id.required": "Click id is required",
        "sdk.money.value.negative": "Money value cannot be negative",
        "sdk.event.builder.type.invalid": "{builder} supports only event_type='{event_type}'",
        "sdk.event.key.required": "Event key is required",
        "sdk.event.payload.invalid": "Invalid event payload",
        "sdk.event.payload.reserved": "Payload contains reserved event keys",
        "sdk.event.revenue.amount.required": "Revenue events require amount",
        "sdk.event.revenue.currency.required": "Revenue events require currency",
        "sdk.event.revenue.currency.invalid": "Revenue event currency must be a 3-letter code",
        "sdk.s2s.app_code.unknown": "Unknown app code '{app_code}'",
        "sdk.s2s.platform.not_configured": "Platform '{platform}' is not configured for app '{app_code}'",
        "sdk.s2s.platform.invalid": "Resolved platform is invalid",
        "sdk.s2s.signature.mismatch": "Request signature is invalid",
        "metric.money.value": "Metric events cannot carry money values",
        "conversion.money.value": "Non-revenue conversion events cannot carry money values",
        "domain.click.status.invalid": "Click status is invalid",
        "domain.click.platform.invalid": "Click platform does not match",
        "domain.statistics.amount.currency.invalid": "Statistics aggregate amount currency must be USD",
    }

    def resolve(self, key: str, context: Dict[str, Any]) -> str:
        return self.CATALOG.get(key, "Internal server error").format(**context)
