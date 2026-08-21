import pytest
from app.services.digital_twin_lab.defense_path_simulation_engine import DefensePathSimulationEngine

def test_response_what_if_interception():
    engine = DefensePathSimulationEngine()
    res = engine.evaluate_defense_interception(["ast_api_gw", "ast_auth_cluster"], ["ctl_waf_gateway"])
    assert res["is_contained"] is True
    assert len(res["intercepted_points"]) >= 1
