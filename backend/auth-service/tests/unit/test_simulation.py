import pytest
from app.services.security_engineering.security_simulation_engine import SecuritySimulationEngine

def test_simulation_before_after():
    engine = SecuritySimulationEngine()
    sim = engine.simulate_improvement(
        improvement_id="imp_test",
        before_state={"detection_coverage": 0.90},
        simulated_change={"add_rule": "sigma_t1055"},
    )
    assert sim.status == "SIMULATED_SUCCESS"
    assert sim.after_state["detection_coverage"] == 0.94
    assert sim.digital_twin_verified is True
