"""Unit tests for Risk Engine Metrics & Performance Controls (Phase 3.9 Part 1B)."""

import pytest
from app.schemas.risk_aggregation_models import RiskMetricsDTO


def test_risk_metrics_dto():
    metrics = RiskMetricsDTO(
        assessments_evaluated=100,
        high_risk_assessments=15,
        critical_risk_assessments=2,
        insufficient_evidence_assessments=5,
    )

    assert metrics.assessments_evaluated == 100
    assert metrics.high_risk_assessments == 15
