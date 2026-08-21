import pytest
from app.services.global_intelligence.threat_exposure_matrix_engine import ThreatExposureMatrixEngine

def test_threat_asset_exposure_correlation():
    engine = ThreatExposureMatrixEngine()
    res = engine.evaluate_exposure("cmp_darkstorm_2026", ["ast_api_gw", "ast_auth_cluster"])
    assert res["exposure_score"] >= 0.80
    assert res["claim_status"] == "CORRELATED"
