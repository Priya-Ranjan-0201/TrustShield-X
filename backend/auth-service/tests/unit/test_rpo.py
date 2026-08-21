import pytest
from app.services.resilience.rpo_rto_engine import RPORTOEngine

def test_rpo():
    engine = RPORTOEngine()
    unverified = engine.evaluate_rpo("svc_test", 15, None, is_empirically_tested=False)
    assert unverified.validation_status == "NOT_VERIFIED"
    verified = engine.evaluate_rpo("svc_test", 15, 4.0, is_empirically_tested=True)
    assert verified.validation_status == "VERIFIED"
