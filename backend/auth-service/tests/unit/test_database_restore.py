import pytest
from app.services.resilience.dr_drill_engine import DisasterRecoveryDrillEngine

def test_database_restore():
    engine = DisasterRecoveryDrillEngine()
    drill = engine.schedule_drill(drill_type="DATABASE_RESTORE", environment="ISOLATED_SANDBOX")
    assert drill.drill_type == "DATABASE_RESTORE"
    assert drill.status == "RUNNING"
    completed = engine.complete_drill(drill.drill_id, measured_rto=12.0, measured_rpo=3.0)
    assert completed.status == "COMPLETED"
