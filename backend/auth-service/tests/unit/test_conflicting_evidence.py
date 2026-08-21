"""Unit tests for Contradictory Evidence Preservation (Phase 3.9 Part 1C)."""

import pytest
from app.services.risk_decision_engine import RiskDecisionEngine


def test_conflicting_evidence_state():
    engine = RiskDecisionEngine()
    state, rec = engine.evaluate_decision_state(
        score=50.0,
        confidence_level="LOW",
        evidence_sufficiency="SUFFICIENT",
        contradiction_count=2,
    )

    assert state == "CONFLICTED_ASSESSMENT"
    assert rec == "ADDITIONAL_EVIDENCE_RECOMMENDED"
