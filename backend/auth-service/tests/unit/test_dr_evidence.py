import pytest
from app.services.resilience.rpo_rto_engine import RPORTOEngine

def test_dr_evidence_status():
    engine = RPORTOEngine()
    rto = engine.evaluate_rto("svc_auth", target_rto_minutes=30, measured_time_minutes=12.0, is_empirically_tested=True)
    assert rto.validation_status == "VERIFIED"
    assert rto.evidence_reference == "ev_drill_rto_svc_auth"
