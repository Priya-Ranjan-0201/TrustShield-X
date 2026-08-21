import pytest
from app.services.digital_twin_lab.twin_drift_engine import TwinDriftEngine

def test_twin_drift_detection_and_reconciliation():
    engine = TwinDriftEngine()
    drifts = engine.list_drifts()
    assert len(drifts) >= 1
    
    reconciled = engine.reconcile_drift("twdr_api_ratelimit_drift")
    assert reconciled is not None
    assert reconciled.is_reconciled is True
