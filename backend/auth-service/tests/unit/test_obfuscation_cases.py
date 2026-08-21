"""Unit tests for Obfuscated Application Scenarios (Phase 3.9 Part 1C)."""

import pytest
from app.services.risk_aggregation_engine import RiskAggregationEngine


def test_obfuscated_app_risk():
    engine = RiskAggregationEngine()
    ass, factors, cat_scores, contribs, intr, mit, prot, cfl = engine.calculate_risk([])

    assert ass.risk_band != "CRITICAL_RISK"
