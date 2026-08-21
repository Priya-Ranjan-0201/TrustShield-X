import pytest
from app.services.security_engineering.outcome_measurement_engine import OutcomeMeasurementEngine

def test_outcome_measurement():
    engine = OutcomeMeasurementEngine()
    # 1. Lower is better (e.g. false positive rate)
    improved = engine.measure_outcome("imp_1", baseline_metric=0.08, expected_metric=0.02, actual_metric=0.02)
    assert improved.outcome_status == "IMPROVED"

    # 2. Degraded
    degraded = engine.measure_outcome("imp_2", baseline_metric=0.08, expected_metric=0.02, actual_metric=0.12)
    assert degraded.outcome_status == "DEGRADED"
