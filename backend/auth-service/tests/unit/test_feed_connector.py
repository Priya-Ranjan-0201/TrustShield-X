"""Unit Tests — Threat Intelligence Providers & Connectors (Phase 4.0 Part 6 — Sections 2-5, 115)."""

import pytest
from app.schemas.continuous_intelligence_models import ThreatFeedConfigurationDTO
from app.services.monitoring.threat_intelligence_provider import (
    JSONFeedProvider,
    CSVFeedProvider,
    STIXTAXIIProvider,
    LocalDatabaseProvider,
    SSRFValidationError,
)


class TestThreatFeedConnectors:
    def test_json_feed_provider_fetches_indicators(self):
        config = ThreatFeedConfigurationDTO(
            feed_id="feed_json_01",
            provider_name="PhishFeed JSON",
            provider_type="JSON_FEED",
            endpoint="https://phishfeed.security.internal/api/v1/indicators",
        )
        mock_data = [
            {"id": "ioc_1", "type": "DOMAIN", "value": "phishing-bank.in", "classification": "MALICIOUS"},
            {"id": "ioc_2", "type": "URL", "value": "https://fake-login.com/auth", "classification": "MALICIOUS"},
        ]
        provider = JSONFeedProvider(config, mock_data=mock_data)
        indicators = provider.fetch_indicators()
        assert len(indicators) == 2
        assert indicators[0]["value"] == "phishing-bank.in"

    def test_csv_feed_provider_parsing(self):
        config = ThreatFeedConfigurationDTO(
            feed_id="feed_csv_01",
            provider_name="Blocklist CSV",
            provider_type="CSV_FEED",
            endpoint="https://blocklist.security.internal/feed.csv",
        )
        mock_rows = [
            ["ioc_10", "DOMAIN", "malicious-c2.net", "MALICIOUS"],
            ["ioc_11", "HASH", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "MALICIOUS"],
        ]
        provider = CSVFeedProvider(config, mock_csv_rows=mock_rows)
        indicators = provider.fetch_indicators()
        assert len(indicators) == 2
        assert indicators[0]["raw_value"] == "malicious-c2.net"

    def test_ssrf_protection_blocks_internal_metadata_and_loopback(self):
        # Localhost blocked
        config_loopback = ThreatFeedConfigurationDTO(
            feed_id="feed_ssrf_01",
            provider_name="Malicious Feed",
            provider_type="JSON_FEED",
            endpoint="http://127.0.0.1:8000/internal",
        )
        with pytest.raises(SSRFValidationError):
            JSONFeedProvider(config_loopback)

        # Cloud metadata blocked
        config_cloud = ThreatFeedConfigurationDTO(
            feed_id="feed_ssrf_02",
            provider_name="Metadata Stealer",
            provider_type="JSON_FEED",
            endpoint="http://169.254.169.254/latest/meta-data",
        )
        with pytest.raises(SSRFValidationError):
            JSONFeedProvider(config_cloud)
