import pytest
from app.services.global_intelligence.threat_exposure_matrix_engine import ThreatExposureMatrixEngine

def test_threat_control_coverage_matrix():
    engine = ThreatExposureMatrixEngine()
    res = engine.evaluate_exposure("cmp_generic", ["ast_unimportant_worker"])
    assert res["control_coverage_score"] >= 0.85
