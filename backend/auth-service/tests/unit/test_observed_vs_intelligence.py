"""Unit tests for Separation of Observed Indicator vs Intelligence Match (Phase 3.9 Part 1A.23)."""

import pytest
from app.schemas.threat_intelligence_models import ThreatIndicatorDTO, ThreatMatchDTO


def test_observed_vs_intelligence_separation():
    ind = ThreatIndicatorDTO(
        indicator_id="ind_1",
        indicator_type="DOMAIN",
        normalized_value="example.com",
        display_value="example.com",
        value_hash="hash_1",
        source_module="NETWORK",
        source_location="com.bank.Net",
    )
    match = ThreatMatchDTO(
        match_id="m_1",
        indicator_id=ind.indicator_id,
        source_id="src_feed",
        match_type="EXACT_MATCH",
        reputation="PHISHING_REPORTED",
        provenance="Feed v1",
    )

    assert ind.indicator_id == match.indicator_id
    assert ind.normalized_value == "example.com"
    assert match.reputation == "PHISHING_REPORTED"
