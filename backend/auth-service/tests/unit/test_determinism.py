"""Unit tests for Pipeline Score Determinism (Phase 3.9 Part 1C)."""

import pytest
from app.services.risk_aggregation_engine import RiskAggregationEngine


def test_score_determinism_multi_run():
    engine = RiskAggregationEngine()
    ass1, _, _, _, _, _, _, _ = engine.calculate_risk([])
    ass2, _, _, _, _, _, _, _ = engine.calculate_risk([])

    assert ass1.risk_score == ass2.risk_score
    assert ass1.risk_band == ass2.risk_band
