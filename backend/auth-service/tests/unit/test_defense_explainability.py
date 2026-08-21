import pytest
from app.services.adaptive_defense.adaptive_defense_fabric import AdaptiveDefenseFabric


def test_defense_decision_explainability_structure():
    fabric = AdaptiveDefenseFabric()
    rec = fabric.create_recommendation(
        tenant_id="tenant_exp",
        title="Block External Command Node",
        action_classification="NETWORK_CONTROL",
        target_resource="198.51.100.88",
    )

    sim = fabric.simulation.simulate_adaptation(rec)
    decision = fabric.decision.evaluate_decision(rec, sim, has_human_approval=True)

    assert "why" in decision.explanation
    assert "evidence" in decision.explanation
    assert "risk" in decision.explanation
    assert "approval" in decision.explanation
