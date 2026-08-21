import pytest
from app.services.resilience.safe_automated_recovery_engine import SafeAutomatedRecoveryEngine

def test_recovery_budget():
    engine = SafeAutomatedRecoveryEngine()
    res = engine.is_action_safe_for_automation("RESTART_POD", is_reversible=True, estimated_blast_radius=2)
    assert res["allowed"] is True
    blocked = engine.is_action_safe_for_automation("DROP_DATABASE", is_reversible=False, estimated_blast_radius=10)
    assert blocked["allowed"] is False
