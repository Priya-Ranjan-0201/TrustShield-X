import pytest
from app.services.cyber_digital_twin.action_verification_rollback_engine import ActionVerificationRollbackEngine

def test_automatic_rollback():
    engine = ActionVerificationRollbackEngine()
    roll = engine.trigger_rollback("ROLL-01", "ACT-01", "t1", "DEV-01", "UNQUARANTINE", {"revert_confirmed": True})
    assert roll["status"] == "ROLLED_BACK"
