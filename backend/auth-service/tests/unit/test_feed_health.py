import pytest
from app.services.threat_intelligence.feed_health_engine import FeedHealthEngine


def test_feed_health_stale_and_expired_marking():
    engine = FeedHealthEngine()

    # Normal feed
    h_healthy = engine.record_feed_metrics("feed_1", availability_pct=99.9, success_rate_pct=99.5)
    assert h_healthy.freshness_state == "CURRENT"

    # Failing feed (drops below 80% success) -> marked STALE
    h_stale = engine.record_feed_metrics("feed_failing", availability_pct=85.0, success_rate_pct=72.0)
    assert h_stale.freshness_state == "STALE"
