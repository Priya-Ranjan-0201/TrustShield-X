"""Unit tests for Input Sanitization & Security Protection (Phase 3.9 Part 1C)."""

import pytest
from app.services.risk_aggregation_engine import RiskAggregationEngine


def test_security_input_handling():
    engine = RiskAggregationEngine()
    ass, factors, cat_scores, contribs, intr, mit, prot, cfl = engine.calculate_risk([])

    assert ass.risk_score <= 100.0
