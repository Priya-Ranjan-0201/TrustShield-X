import pytest
from app.services.zero_trust_exposure.continuous_exposure_monitoring_engine import ContinuousExposureMonitoringEngine

def test_exposure_drift_newly_exposed():
    engine = ContinuousExposureMonitoringEngine()
    drift = engine.check_exposure_drift(
        drift_id="D-2",
        tenant_id="t1",
        asset_id="STORAGE-1",
        previous_state={"exposed_publicly": False},
        current_state={"exposed_publicly": True}
    )
    assert drift["drift_type"] == "EXPOSURE_DRIFT"
