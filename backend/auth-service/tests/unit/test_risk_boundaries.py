"""Unit tests for Exact Risk Band Boundary Thresholds (Phase 3.9 Part 1C)."""

import pytest
from app.services.risk_decision_engine import RiskDecisionEngine


def test_exact_risk_band_boundaries():
    engine = RiskDecisionEngine()

    assert engine.map_score_to_band(20.0) == "TRUSTED"
    assert engine.map_score_to_band(21.0) == "LOW_RISK"
    assert engine.map_score_to_band(40.0) == "LOW_RISK"
    assert engine.map_score_to_band(41.0) == "MODERATE_RISK"
    assert engine.map_score_to_band(60.0) == "MODERATE_RISK"
    assert engine.map_score_to_band(61.0) == "HIGH_RISK"
    assert engine.map_score_to_band(80.0) == "HIGH_RISK"
    assert engine.map_score_to_band(81.0) == "CRITICAL_RISK"
