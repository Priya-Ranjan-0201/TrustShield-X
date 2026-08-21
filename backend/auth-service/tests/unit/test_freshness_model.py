"""Unit tests for Intelligence Freshness Model (Phase 3.9 Part 1A.23)."""

import pytest
from app.schemas.threat_intelligence_models import ThreatMatchDTO


def test_freshness_model_dto():
    match_stale = ThreatMatchDTO(
        match_id="m_stale",
        indicator_id="ind_stale",
        source_id="src_stale",
        match_type="EXACT_MATCH",
        reputation="SUSPICIOUS",
        freshness_state="STALE",
        provenance="Old Feed",
    )

    assert match_stale.freshness_state == "STALE"
