import pytest
from app.services.cyber_digital_twin.what_if_simulation_engine import WhatIfSimulationEngine

def test_defense_action_simulation():
    engine = WhatIfSimulationEngine()
    res = engine.run_what_if("DEF-SIM-01", "t1", "K8S-NODE-01", "ISOLATE_DEVICE", baseline_risk=8.0)
    assert res["is_simulation"] is True
    assert res["risk_change"] == -6.0
    assert res["simulated_state_summary"]["risk_score"] == 2.0
