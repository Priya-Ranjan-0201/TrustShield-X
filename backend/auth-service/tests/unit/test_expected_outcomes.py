import pytest
from app.services.security_engineering.outcome_measurement_engine import OutcomeMeasurementEngine

def test_expected_outcomes():
    engine = OutcomeMeasurementEngine()
    res = engine.measure_outcome("imp_test", baseline_metric=0.10, expected_metric=0.02, actual_metric=0.015)
    assert res.outcome_status == "IMPROVED"
    assert res.risk_reduction_score > 0
