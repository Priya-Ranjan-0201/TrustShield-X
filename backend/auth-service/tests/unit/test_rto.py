import pytest
from app.services.resilience.rpo_rto_engine import RPORTOEngine

def test_rto():
    engine = RPORTOEngine()
    unverified = engine.evaluate_rto("svc_test", 30, None, is_empirically_tested=False)
    assert unverified.validation_status == "NOT_VERIFIED"
    verified = engine.evaluate_rto("svc_test", 30, 14.5, is_empirically_tested=True)
    assert verified.validation_status == "VERIFIED"
