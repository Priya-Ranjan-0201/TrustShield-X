import pytest
from app.services.soc.soc_scorecard_engine import SOCScorecardEngine


def test_soc_metrics_aggregation():
    engine = SOCScorecardEngine()
    scorecard = engine.compute_scorecard("tenant_metrics")

    assert scorecard.alert_volume > 1000
    assert scorecard.true_positive_rate_pct > 90.0
    assert scorecard.scorecard_grade == "EXCELLENT"
