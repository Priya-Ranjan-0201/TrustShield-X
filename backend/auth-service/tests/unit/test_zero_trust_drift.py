import pytest
from app.services.zero_trust_exposure.continuous_exposure_monitoring_engine import ContinuousExposureMonitoringEngine

def test_zero_trust_policy_drift():
    engine = ContinuousExposureMonitoringEngine()
    drift = engine.check_exposure_drift(
        drift_id="D-3",
        tenant_id="t1",
        asset_id="DEV-POLICY-1",
        previous_state={"trust_state": "TRUSTED"},
        current_state={"trust_state": "UNTRUSTED"}
    )
    assert drift["drift_type"] == "ZERO_TRUST_DRIFT"
