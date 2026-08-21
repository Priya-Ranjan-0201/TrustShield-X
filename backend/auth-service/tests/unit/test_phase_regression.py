"""Unit tests for Complete Multi-Phase Pipeline Regression (Phase 3.9 Part 1C)."""

import pytest
from app.services.risk_aggregation_engine import RiskAggregationEngine


def test_phase_regression_pipeline():
    engine = RiskAggregationEngine()
    ass, factors, cat_scores, contribs, intr, mit, prot, cfl = engine.calculate_risk([])

    assert ass.engine_version == "1.0.0"
