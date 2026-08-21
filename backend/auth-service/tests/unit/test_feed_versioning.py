"""Unit tests for Feed Versioning (Phase 3.9 Part 1A.23)."""

import pytest
from app.schemas.threat_intelligence_models import ThreatFeedDTO


def test_feed_versioning_dto():
    feed = ThreatFeedDTO(
        feed_id="feed_1",
        feed_name="OpenIOC",
        provider="OpenProvider",
        version="2.0.1",
        record_count=100,
        freshness_state="CURRENT",
    )

    assert feed.version == "2.0.1"
    assert feed.freshness_state == "CURRENT"
