import pytest
from app.services.resilience.dr_drill_engine import DisasterRecoveryDrillEngine

def test_failover():
    engine = DisasterRecoveryDrillEngine()
    drill = engine.schedule_drill("SERVICE_FAILOVER", environment="ISOLATED_SANDBOX")
    completed = engine.complete_drill(drill.drill_id, measured_rto=5.0, measured_rpo=0.0)
    assert completed.measured_rto_minutes == 5.0
