import pytest
from app.services.digital_twin_lab.what_if_analysis_engine import WhatIfAnalysisEngine

def test_detection_what_if_analysis():
    engine = WhatIfAnalysisEngine()
    res = engine.simulate_detection_what_if({"sigma_id": "rule_t1055_v2"})
    assert res["dimension"] == "DETECTION_CHANGE"
    assert res["projected_coverage_gain"] == 0.04
