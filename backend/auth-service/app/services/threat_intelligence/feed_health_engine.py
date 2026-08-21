"""
TruthShield X — Feed Health Engine (Phase 22).

Tracks feed availability, latency, schema rejection rates, duplicate rates, and automatic stale markings.
"""

from typing import Dict, Optional
from datetime import datetime, timezone
from app.schemas.threat_intelligence_fabric_models import FeedHealthDTO


class FeedHealthEngine:
    """Evaluates telemetry and health status of external and internal threat feeds."""

    def __init__(self):
        self._health_records: Dict[str, FeedHealthDTO] = {}

    def record_feed_metrics(
        self,
        feed_id: str,
        availability_pct: float = 99.9,
        success_rate_pct: float = 99.8,
        latency_ms: float = 85.0,
        schema_errors: int = 0,
        duplicate_rate_pct: float = 1.0,
        rejection_rate_pct: float = 0.2,
        volume: int = 50000,
    ) -> FeedHealthDTO:
        freshness = "CURRENT"
        if success_rate_pct < 80.0 or availability_pct < 90.0:
            freshness = "STALE"
        if success_rate_pct < 50.0:
            freshness = "EXPIRED"

        dto = FeedHealthDTO(
            feed_id=feed_id,
            availability_pct=availability_pct,
            ingestion_success_rate_pct=success_rate_pct,
            latency_ms=latency_ms,
            freshness_state=freshness,
            schema_errors_count=schema_errors,
            duplicate_rate_pct=duplicate_rate_pct,
            rejection_rate_pct=rejection_rate_pct,
            object_volume=volume,
            evaluated_at=datetime.now(timezone.utc).isoformat(),
        )
        self._health_records[feed_id] = dto
        return dto

    def get_feed_health(self, feed_id: str) -> FeedHealthDTO:
        if feed_id not in self._health_records:
            return self.record_feed_metrics(feed_id)
        return self._health_records[feed_id]
