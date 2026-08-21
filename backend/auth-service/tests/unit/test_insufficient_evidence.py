"""Unit tests for Insufficient Evidence Decision State (Phase 3.9 Part 1B)."""

import pytest
from app.services.risk_decision_engine import RiskDecisionEngine


def test_insufficient_evidence_state():
    engine = RiskDecisionEngine()
    state, rec = engine.evaluate_decision_state(
        score=75.0,
        confidence_level="LOW",
        evidence_sufficiency="INSUFFICIENT",
    )

    assert state == "INSUFFICIENT_EVIDENCE"
    assert rec == "LOW_CONFIDENCE"
