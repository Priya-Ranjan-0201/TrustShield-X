import pytest
from app.services.resilience.dr_drill_engine import DisasterRecoveryDrillEngine

def test_queue_recovery():
    engine = DisasterRecoveryDrillEngine()
    drill = engine.schedule_drill(drill_type="QUEUE_FAILURE", environment="ISOLATED_SANDBOX")
    assert drill.drill_type == "QUEUE_FAILURE"
    completed = engine.complete_drill(drill.drill_id, measured_rto=4.0, measured_rpo=0.5)
    assert completed.status == "COMPLETED"
