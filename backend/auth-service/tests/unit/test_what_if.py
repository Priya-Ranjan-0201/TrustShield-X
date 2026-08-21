import pytest
from app.services.cyber_digital_twin.what_if_simulation_engine import WhatIfSimulationEngine

def test_what_if_patch_vulnerability():
    engine = WhatIfSimulationEngine()
    res = engine.run_what_if("WHAT-IF-01", "t1", "API-GW", "PATCH_VULNERABILITY", baseline_risk=8.5, baseline_attack_paths_count=5)
    assert res["simulated_state_summary"]["risk_score"] == 4.0
    assert res["attack_path_change"]["paths_removed"] == 3
