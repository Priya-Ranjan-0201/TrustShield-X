import pytest
from app.services.digital_twin_lab.cyber_defense_digital_twin_engine import CyberDefenseDigitalTwinEngine

def test_security_engineering_twin_branching_and_what_if():
    engine = CyberDefenseDigitalTwinEngine()
    branch = engine.state_engine.create_branch("twstate_v1_prod_sync", "branch_improvement_01", {"new_rule": "SIGMA_T1055"})
    what_if = engine.what_if_engine.simulate_detection_what_if({"sigma_id": "SIGMA_T1055"})
    assert branch.branch_name == "branch_improvement_01"
    assert what_if["projected_coverage_gain"] == 0.04
