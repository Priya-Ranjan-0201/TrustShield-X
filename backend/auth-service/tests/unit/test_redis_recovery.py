import pytest
from app.services.resilience.dr_drill_engine import DisasterRecoveryDrillEngine

def test_redis_recovery():
    engine = DisasterRecoveryDrillEngine()
    drill = engine.schedule_drill(drill_type="CACHE_FAILURE", environment="ISOLATED_SANDBOX")
    assert drill.drill_type == "CACHE_FAILURE"
    completed = engine.complete_drill(drill.drill_id, measured_rto=2.5, measured_rpo=0.0)
    assert completed.measured_rto_minutes == 2.5
