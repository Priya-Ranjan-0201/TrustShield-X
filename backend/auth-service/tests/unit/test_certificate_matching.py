"""Unit tests for Signing Certificate Matching (Phase 3.9 Part 1A.23)."""

import pytest
from app.schemas.threat_intelligence_models import ThreatMatchDTO


def test_certificate_match_dto():
    match = ThreatMatchDTO(
        match_id="m_cert",
        indicator_id="ind_cert",
        source_id="src_db",
        match_type="CERTIFICATE_MATCH",
        reputation="MALICIOUS_REPORTED",
        provenance="IOC Feed",
    )

    assert match.match_type == "CERTIFICATE_MATCH"
