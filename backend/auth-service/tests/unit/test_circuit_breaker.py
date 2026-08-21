import pytest
from app.services.cyber_digital_twin.action_verification_rollback_engine import ActionVerificationRollbackEngine

def test_circuit_breaker_tripping():
    engine = ActionVerificationRollbackEngine()
    
    # Normal under 3 failures
    cb1 = engine.check_circuit_breaker("t1", recent_failure_count=2)
    assert cb1["circuit_breaker_tripped"] is False
    
    # Trips on 3 failures
    cb2 = engine.check_circuit_breaker("t1", recent_failure_count=3)
    assert cb2["circuit_breaker_tripped"] is True
    assert cb2["action_permitted"] is False
