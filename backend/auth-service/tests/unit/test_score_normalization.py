"""Unit tests for Score Normalization to [0, 100] Range (Phase 3.9 Part 1B)."""

import pytest
from app.services.risk_decision_engine import RiskDecisionEngine


def test_score_normalization_bounds():
    engine = RiskDecisionEngine()
    assert engine.map_score_to_band(-10.0) == "TRUSTED"
    assert engine.map_score_to_band(150.0) == "CRITICAL_RISK"
