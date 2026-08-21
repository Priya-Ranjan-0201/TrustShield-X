"""Unit tests for Score Overflow/Underflow Normalization (Phase 3.9 Part 1C)."""

import pytest
from app.services.risk_decision_engine import RiskDecisionEngine


def test_score_bounds_normalization():
    engine = RiskDecisionEngine()

    assert engine.map_score_to_band(-100.0) == "TRUSTED"
    assert engine.map_score_to_band(1000.0) == "CRITICAL_RISK"
