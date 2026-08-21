import pytest
from app.services.global_intelligence.threat_exposure_matrix_engine import ThreatExposureMatrixEngine

def test_security_assurance_control_verification_link():
    engine = ThreatExposureMatrixEngine()
    res = engine.evaluate_exposure("cmp_darkstorm_2026", ["ast_api_gw"])
    assert "Phase 24" in res["recommended_action"]
