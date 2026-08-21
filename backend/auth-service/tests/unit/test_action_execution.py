import pytest
from app.services.cyber_digital_twin.autonomous_defense_engine import AutonomousDefenseEngine

def test_action_execution_flow():
    engine = AutonomousDefenseEngine()
    act = engine.propose_defensive_action("ACT-EXEC", "t1", "DEV-02", "QUARANTINE_NON_CRITICAL_ENDPOINT")
    engine.record_approval("ACT-EXEC", "t1", "APPROVER-1")
    
    executed = engine.execute_action("ACT-EXEC", "t1")
    assert executed["status"] == "EXECUTED"
    assert executed["execution_result"]["success"] is True
