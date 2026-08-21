import pytest
from app.services.resilience_twin.control_effectiveness_engine import ControlEffectivenessEngine


def test_control_effectiveness_modeling():
    engine = ControlEffectivenessEngine()

    waf_eff = engine.evaluate_control_effectiveness("WAF_SHIELD")
    assert waf_eff["preventive_effect"] >= 0.85
    assert waf_eff["status"] == "ESTIMATED"

    edr_eff = engine.evaluate_control_effectiveness("EDR_AGENT")
    assert edr_eff["containment_effect"] >= 0.90
