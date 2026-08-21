"""Unit tests for Large Feed Performance & Scaling (Phase 3.9 Part 1A.23)."""

import pytest
from app.schemas.threat_intelligence_models import ThreatMetricsDTO


def test_large_feed_metrics_dto():
    metrics = ThreatMetricsDTO(
        indicators_processed=100000,
        matches_count=50,
        conflicts_count=2,
        expired_indicators_count=10,
    )

    assert metrics.indicators_processed == 100000
