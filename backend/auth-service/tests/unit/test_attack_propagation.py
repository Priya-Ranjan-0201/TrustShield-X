import pytest
from app.services.resilience_twin.attack_propagation_engine import AttackPropagationEngine


def test_four_step_attack_propagation_trajectory():
    engine = AttackPropagationEngine()
    traj = engine.project_propagation_path("scen_phishing_01", "ep-workstation-42")

    assert traj.target_resource == "ep-workstation-42"
    assert len(traj.steps) == 4

    step_names = [s["step"] for s in traj.steps]
    assert step_names == ["CURRENT", "+1 STEP", "+2 STEPS", "+3 STEPS"]

    for s in traj.steps:
        assert s["label"] in ("SIMULATED", "PREDICTED")
        assert 0.0 <= s["confidence"] <= 1.0
