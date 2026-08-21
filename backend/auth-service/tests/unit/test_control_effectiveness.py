import pytest
from app.services.cyber_digital_twin.what_if_simulation_engine import WhatIfSimulationEngine

def test_control_effectiveness_microsegmentation():
    engine = WhatIfSimulationEngine()
    res = engine.run_what_if("EFF-01", "t1", "APP-ZONE", "ADD_MICROSEGMENTATION", baseline_risk=8.0)
    assert res["risk_change"] == -5.5
    assert res["simulated_state_summary"]["risk_score"] == 2.5
