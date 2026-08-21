import pytest
from app.services.zero_trust_exposure.continuous_exposure_monitoring_engine import ContinuousExposureMonitoringEngine

def test_policy_drift_detection():
    engine = ContinuousExposureMonitoringEngine()
    
    # Baseline
    b = engine.record_baseline("tenant-alpha", {"open_ports": [443], "unapproved_admins": 0})
    assert b["status"] == "BASELINE_ACTIVE"
    
    # Observation with drift (port 22 opened, 2 unapproved admins)
    obs = engine.evaluate_drift("tenant-alpha", {"open_ports": [443, 22], "unapproved_admins": 2})
    assert obs["drift_detected"] is True
    assert len(obs["drifts"]) >= 1
