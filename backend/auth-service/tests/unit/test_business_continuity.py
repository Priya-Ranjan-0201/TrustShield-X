import pytest
from app.services.resilience.rpo_rto_engine import RPORTOEngine

def test_business_continuity_integration():
    engine = RPORTOEngine()
    rto = engine.evaluate_rto("svc_auth", target_rto_minutes=30, measured_time_minutes=12.0, is_empirically_tested=True)
    rpo = engine.evaluate_rpo("svc_auth", target_rpo_minutes=15, measured_loss_minutes=0.5, is_empirically_tested=True)
    assert rto.validation_status == "VERIFIED"
    assert rpo.validation_status == "VERIFIED"
