import pytest
from app.services.cyber_digital_twin.what_if_simulation_engine import WhatIfSimulationEngine

def test_control_failure_simulation():
    engine = WhatIfSimulationEngine()
    res = engine.run_what_if("FAIL-SIM-01", "t1", "FIREWALL", "SIMULATE_CONTROL_FAILURE", baseline_risk=5.0)
    assert res["risk_change"] == +3.5
    assert res["simulated_state_summary"]["risk_score"] == 8.5
