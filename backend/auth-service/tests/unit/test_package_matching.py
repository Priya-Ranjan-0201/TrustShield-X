"""Unit tests for Package Identifier Matching (Phase 3.9 Part 1A.23)."""

import pytest
from app.schemas.threat_intelligence_models import ThreatMatchDTO


def test_package_match_dto():
    match = ThreatMatchDTO(
        match_id="m_pkg",
        indicator_id="ind_pkg",
        source_id="src_db",
        match_type="PACKAGE_MATCH",
        reputation="SUSPICIOUS_REPORTED",
        provenance="IOC Feed",
    )

    assert match.match_type == "PACKAGE_MATCH"
