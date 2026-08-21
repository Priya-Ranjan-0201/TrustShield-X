"""Unit tests for IP Intelligence Matching (Phase 3.9 Part 1A.23)."""

import pytest
from app.schemas.threat_intelligence_models import ThreatMatchDTO


def test_ip_match_dto():
    match = ThreatMatchDTO(
        match_id="m_ip",
        indicator_id="ind_ip",
        source_id="src_db",
        match_type="EXACT_MATCH",
        reputation="SUSPICIOUS_REPORTED",
        provenance="IOC Feed",
    )

    assert match.match_type == "EXACT_MATCH"
