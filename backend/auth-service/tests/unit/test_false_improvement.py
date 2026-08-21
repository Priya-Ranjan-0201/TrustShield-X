import pytest
from app.services.security_engineering.outcome_measurement_engine import OutcomeMeasurementEngine

def test_false_improvement():
    engine = OutcomeMeasurementEngine()
    # If metric is actually degraded, cannot claim IMPROVED
    outcome = engine.measure_outcome("imp_1", baseline_metric=0.05, expected_metric=0.01, actual_metric=0.10)
    assert outcome.outcome_status == "DEGRADED"
