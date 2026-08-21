import pytest
from app.services.resilience_twin.attack_propagation_engine import AttackPropagationEngine


def test_future_states_discrete_sequence():
    engine = AttackPropagationEngine()
    traj = engine.project_propagation_path("scen_ransomware_01", "srv-app-01")

    assert traj.steps[0]["step"] == "CURRENT"
    assert traj.steps[1]["step"] == "+1 STEP"
    assert traj.steps[2]["step"] == "+2 STEPS"
    assert traj.steps[3]["step"] == "+3 STEPS"
