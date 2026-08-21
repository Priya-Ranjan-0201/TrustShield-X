import pytest
from app.services.resilience_twin.attack_scenario_engine import AttackScenarioEngine


def test_scenario_versioning():
    engine = AttackScenarioEngine()
    scens = engine.list_scenarios()
    assert len(scens) >= 3

    for s in scens:
        assert s.version >= 1
        assert len(s.assumptions) >= 1
