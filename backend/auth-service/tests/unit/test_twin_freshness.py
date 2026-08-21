import pytest
from app.services.digital_twin_lab.twin_synchronization_engine import TwinSynchronizationEngine

def test_twin_freshness_thresholds():
    engine = TwinSynchronizationEngine()
    fresh_check = engine.check_freshness(elapsed_seconds=10.0)
    assert fresh_check["freshness_status"] == "FRESH"
    
    stale_check = engine.check_freshness(elapsed_seconds=350.0)
    assert stale_check["freshness_status"] == "STALE_TWIN_STATE"
    assert stale_check["requires_resync"] is True
