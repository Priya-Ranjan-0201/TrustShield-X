"""Unit tests for Hash Matching Engine (Phase 3.9 Part 1A.23)."""

import pytest
from app.schemas.threat_intelligence_models import ThreatMatchDTO


def test_hash_match_dto():
    match = ThreatMatchDTO(
        match_id="m_hash",
        indicator_id="ind_sha256",
        source_id="src_db",
        match_type="HASH_MATCH",
        reputation="MALICIOUS_REPORTED",
        provenance="IOC Feed",
    )

    assert match.match_type == "HASH_MATCH"
