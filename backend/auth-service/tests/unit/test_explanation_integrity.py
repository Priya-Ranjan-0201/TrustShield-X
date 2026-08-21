"""Unit tests for Score Explanation Integrity (Phase 3.9 Part 1C)."""

import pytest
from app.services.risk_aggregation_orchestrator import RiskAggregationOrchestrator


def test_explanation_integrity():
    orchestrator = RiskAggregationOrchestrator()
    res = orchestrator.run_risk_assessment(None)

    assert res.explanation is not None
    assert "Final Cybersecurity Risk Assessment Score" in res.explanation.summary_text
