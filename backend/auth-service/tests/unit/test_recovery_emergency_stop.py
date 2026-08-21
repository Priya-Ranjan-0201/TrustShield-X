import pytest
from app.services.resilience.safe_automated_recovery_engine import SafeAutomatedRecoveryEngine

def test_recovery_emergency_stop():
    engine = SafeAutomatedRecoveryEngine()
    engine.set_emergency_stop(True)
    res = engine.is_action_safe_for_automation("RESTART_POD", is_reversible=True, estimated_blast_radius=1)
    assert res["allowed"] is False
    assert "EMERGENCY_STOP_ACTIVE" in res["reason"]
