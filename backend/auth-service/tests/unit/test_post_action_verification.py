import pytest
from app.services.cyber_digital_twin.action_verification_rollback_engine import ActionVerificationRollbackEngine

def test_post_action_verification():
    engine = ActionVerificationRollbackEngine()
    
    # Verification fails without telemetry proof
    fail = engine.verify_action_execution("VER-01", "ACT-01", "t1", None)
    assert fail["status"] == "NOT_VERIFIED"
    
    # Verification succeeds with independent proof
    succ = engine.verify_action_execution("VER-02", "ACT-01", "t1", {"independent_probe_success": True})
    assert succ["status"] == "VERIFIED"
