"""Unit tests for Evidence Sufficiency Validation (Phase 3.9 Part 1C)."""

import pytest
from app.services.risk_decision_engine import RiskDecisionEngine


def test_evidence_sufficiency_validation():
    engine = RiskDecisionEngine()
    state, rec = engine.evaluate_decision_state(
        score=75.0,
        confidence_level="HIGH",
        evidence_sufficiency="INSUFFICIENT",
    )

    assert state == "INSUFFICIENT_EVIDENCE"
