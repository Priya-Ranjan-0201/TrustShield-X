import pytest
from app.services.cyber_crisis_command.crisis_recovery_engine import CrisisRecoveryEngine

def test_recovery_independent_verification():
    engine = CrisisRecoveryEngine()
    
    # Missing probe fails
    unverified = engine.verify_recovery("C-REC", "t1", None)
    assert unverified["overall_recovery_status"] == "RECOVERY_NOT_VERIFIED"
    assert unverified["verified"] is False
    
    # Valid security probe succeeds
    verified = engine.verify_recovery("C-REC", "t1", {"security_probe_success": True})
    assert verified["overall_recovery_status"] == "RECOVERY_VERIFIED"
    assert verified["verified"] is True
