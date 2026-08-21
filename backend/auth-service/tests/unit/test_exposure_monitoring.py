import pytest
from app.services.zero_trust_exposure.continuous_exposure_monitoring_engine import ContinuousExposureMonitoringEngine

def test_exposure_monitoring():
    engine = ContinuousExposureMonitoringEngine()
    drift = engine.check_exposure_drift(
        drift_id="D-1",
        tenant_id="t1",
        asset_id="ASSET-1",
        previous_state={"open_ports": [443]},
        current_state={"open_ports": [443, 8080]}
    )
    assert drift is not None
    assert drift["drift_type"] == "EXPOSURE_DRIFT"
