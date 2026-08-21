"""Unit Tests — Feed Validation, Normalization & Deduplication (Phase 4.0 Part 6 — Sections 8, 14, 15, 107).

Implements Mandatory Test 1:
- Feed returns the same IOC twice -> exactly one canonical observation.
"""

import pytest
from app.schemas.continuous_intelligence_models import ThreatFeedConfigurationDTO
from app.services.monitoring.feed_validator import FeedValidator, FeedValidationError


class TestFeedValidationAndDeduplication:
    def test_01_mandatory_feed_returns_same_ioc_twice_deduplicates(self):
        config = ThreatFeedConfigurationDTO(
            feed_id="feed_dedup_01",
            provider_name="Test Feed",
            provider_type="JSON_FEED",
            endpoint="https://feed.internal/api",
        )
        item1 = {"id": "1", "type": "DOMAIN", "value": "HTTP://EVIL-PHISHING.COM/"}
        item2 = {"id": "2", "type": "DOMAIN", "value": "https://evil-phishing.com."}

        obs1 = FeedValidator.validate_and_normalize_item(config, item1)
        obs2 = FeedValidator.validate_and_normalize_item(config, item2)
        assert obs1 is not None and obs2 is not None
        assert obs1.normalized_value == "evil-phishing.com"
        assert obs2.normalized_value == "evil-phishing.com"
        assert obs1.indicator_value_hash == obs2.indicator_value_hash

        # Deduplicate
        deduped = FeedValidator.deduplicate_observations([obs1, obs2])
        assert len(deduped) == 1

    def test_oversized_payload_rejected(self):
        large_bytes = b"x" * (51 * 1024 * 1024)
        with pytest.raises(FeedValidationError):
            FeedValidator.validate_feed_size(large_bytes, max_bytes=50 * 1024 * 1024)

    def test_malformed_item_returns_none_safely(self):
        config = ThreatFeedConfigurationDTO(
            feed_id="feed_safe",
            provider_name="Test",
            provider_type="JSON_FEED",
            endpoint="https://feed.internal/api",
        )
        malformed = {"invalid": "key"}
        obs = FeedValidator.validate_and_normalize_item(config, malformed)
        assert obs is None
