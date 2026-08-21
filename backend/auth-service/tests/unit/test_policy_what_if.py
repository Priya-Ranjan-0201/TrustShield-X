import pytest
from app.services.digital_twin_lab.what_if_analysis_engine import WhatIfAnalysisEngine

def test_policy_what_if_analysis():
    engine = WhatIfAnalysisEngine()
    res = engine.simulate_policy_what_if({"rule": "DENY_EXTERNAL_SSH"})
    assert res["dimension"] == "POLICY_CHANGE"
    assert res["projected_unauthorized_access_prevented"] == 3
    assert res["claim_status"] == "MODELED"
