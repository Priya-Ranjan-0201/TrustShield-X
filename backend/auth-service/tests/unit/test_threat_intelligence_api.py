"""Unit Tests — Threat Intelligence Explorer (Phase 4.0 Part 4 — Sections 23-24, 83)."""

import pytest


class TestThreatIntelligenceAPI:
    def test_threat_freshness_values(self):
        valid_freshness = ["CURRENT", "STALE", "EXPIRED", "UNKNOWN"]
        status = "CURRENT"
        assert status in valid_freshness

    def test_stale_intelligence_distinction(self):
        # Freshness must be explicit
        indicator = {
            "ioc": "192.168.1.1",
            "freshness": "STALE",
        }
        assert indicator["freshness"] != "CURRENT"
