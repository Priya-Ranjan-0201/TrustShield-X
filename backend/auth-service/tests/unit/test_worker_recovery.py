import pytest
from app.services.resilience.dr_drill_engine import DisasterRecoveryDrillEngine

def test_worker_recovery():
    engine = DisasterRecoveryDrillEngine()
    drill = engine.schedule_drill(drill_type="WORKER_FAILURE", environment="ISOLATED_SANDBOX")
    completed = engine.complete_drill(drill.drill_id, measured_rto=1.2, measured_rpo=0.0)
    assert completed.measured_rto_minutes == 1.2
