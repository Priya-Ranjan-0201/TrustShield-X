"""Unit tests for Domain Intelligence Matching (Phase 3.9 Part 1A.23)."""

import pytest
from app.schemas.threat_intelligence_models import ThreatMatchDTO


def test_domain_match_dto():
    match = ThreatMatchDTO(
        match_id="m_domain",
        indicator_id="ind_domain",
        source_id="src_db",
        match_type="DOMAIN_MATCH",
        reputation="PHISHING_REPORTED",
        provenance="IOC Feed",
    )

    assert match.match_type == "DOMAIN_MATCH"
