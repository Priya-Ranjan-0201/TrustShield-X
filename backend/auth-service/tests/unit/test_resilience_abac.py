import pytest
from app.services.resilience.safe_automated_recovery_engine import SafeAutomatedRecoveryEngine

def test_resilience_abac():
    engine = SafeAutomatedRecoveryEngine()
    res = engine.is_action_safe_for_automation("SAFE_RESTART", is_reversible=True, estimated_blast_radius=1)
    assert res["allowed"] is True
