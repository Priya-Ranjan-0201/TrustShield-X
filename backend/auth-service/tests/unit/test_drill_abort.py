import pytest
from app.services.resilience.dr_drill_engine import DisasterRecoveryDrillEngine

def test_drill_abort():
    engine = DisasterRecoveryDrillEngine()
    drill = engine.schedule_drill("SERVICE_FAILOVER", environment="ISOLATED_SANDBOX")
    aborted = engine.abort_drill(drill.drill_id, reason="Simulated telemetry loss")
    assert aborted.status == "ABORTED"
    assert aborted.abort_reason == "Simulated telemetry loss"
