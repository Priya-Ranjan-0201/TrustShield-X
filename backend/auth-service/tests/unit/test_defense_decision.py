import pytest
from app.schemas.adaptive_defense_models import AdaptiveControlRecommendationDTO
from app.services.adaptive_defense.defense_decision_engine import DefenseDecisionEngine
from app.services.adaptive_defense.safe_defense_action_registry import SafeDefenseActionRegistry
from app.services.adaptive_defense.adaptive_defense_policy_engine import AdaptiveDefensePolicyEngine


def test_defense_decision_confidence_separation_and_explanation():
    registry = SafeDefenseActionRegistry()
    policy = AdaptiveDefensePolicyEngine()
    engine = DefenseDecisionEngine(registry, policy)

    rec = AdaptiveControlRecommendationDTO(
        title="Block External Attacker IP",
        action_classification="NETWORK_CONTROL",
        target_resource="198.51.100.201",
        automation_level="LEVEL_4_AUTOMATIC_SAFE_ACTION",
    )

    decision = engine.evaluate_decision(rec, has_human_approval=False)
    assert decision.status == "EXECUTE_ALLOWED"
    assert decision.evidence_confidence > 0.8
    assert decision.action_confidence > 0.8
    assert "why" in decision.explanation
    assert "evidence" in decision.explanation
