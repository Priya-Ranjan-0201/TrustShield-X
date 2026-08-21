"""Unit tests for Command-and-Control Infrastructure Matching (Phase 3.9 Part 1A.23)."""

import pytest
from app.schemas.threat_intelligence_models import ThreatMatchDTO


def test_c2_match_dto():
    match = ThreatMatchDTO(
        match_id="m_c2",
        indicator_id="ind_c2_domain",
        source_id="src_db",
        match_type="DOMAIN_MATCH",
        reputation="C2_REPORTED",
        provenance="IOC Feed",
    )

    assert match.reputation == "C2_REPORTED"
