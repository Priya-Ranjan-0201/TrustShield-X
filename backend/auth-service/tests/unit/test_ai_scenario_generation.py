import pytest
from app.services.resilience_twin.attack_scenario_engine import AttackScenarioEngine


def test_ai_scenario_generation_tagging():
    engine = AttackScenarioEngine()
    scen = engine.register_scenario(
        scenario_type="MULTI_MODAL_DEEPFAKE_HEIST",
        assumptions=["CEO voice clone and forged PDF authorization"],
        affected_assets=["treasury_wire_gateway"],
        is_ai_generated=True,
    )

    assert scen.is_ai_generated is True
