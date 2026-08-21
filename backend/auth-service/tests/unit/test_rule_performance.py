"""Unit tests for Rule Performance Controls & Metrics (Phase 3.9 Part 1A.24)."""

import pytest
from app.schemas.behavior_rule_models import RuleMetricsDTO


def test_rule_metrics_dto():
    metrics = RuleMetricsDTO(
        rules_loaded=500,
        rules_evaluated=500,
        rules_matched=45,
        rules_partially_matched=10,
        rules_not_evaluable=5,
        rules_suppressed=2,
        rules_conflicted=1,
    )

    assert metrics.rules_loaded == 500
    assert metrics.rules_matched == 45
