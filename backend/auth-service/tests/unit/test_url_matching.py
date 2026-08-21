"""Unit tests for URL Intelligence Matching (Phase 3.9 Part 1A.23)."""

import pytest
from app.schemas.threat_intelligence_models import ThreatMatchDTO


def test_url_match_dto():
    match = ThreatMatchDTO(
        match_id="m_url",
        indicator_id="ind_url",
        source_id="src_db",
        match_type="URL_MATCH",
        reputation="PHISHING_REPORTED",
        provenance="IOC Feed",
    )

    assert match.match_type == "URL_MATCH"
