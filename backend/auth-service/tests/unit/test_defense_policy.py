import pytest
from app.schemas.adaptive_defense_models import AdaptiveControlRecommendationDTO
from app.services.adaptive_defense.adaptive_defense_policy_engine import AdaptiveDefensePolicyEngine


def test_defense_policy_four_eyes_requirement():
    policy = AdaptiveDefensePolicyEngine()
    rec = AdaptiveControlRecommendationDTO(
        title="Isolate host",
        action_classification="ASSET_ISOLATION",
        target_resource="ep-01",
        automation_level="LEVEL_2_HUMAN_APPROVAL",
    )

    # Without approval
    res_no_app = policy.evaluate_action_policy(rec, has_human_approval=False)
    assert res_no_app["decision"] == "APPROVAL_REQUIRED"

    # With approval
    res_app = policy.evaluate_action_policy(rec, has_human_approval=True)
    assert res_app["decision"] == "EXECUTE_ALLOWED"


def test_defense_policy_explicit_deny():
    policy = AdaptiveDefensePolicyEngine()
    policy.add_explicit_deny("TARGET", "ep-vip-board", "VIP asset freeze")

    rec = AdaptiveControlRecommendationDTO(
        title="Isolate VIP host",
        action_classification="ASSET_ISOLATION",
        target_resource="ep-vip-board-01",
    )

    res = policy.evaluate_action_policy(rec, has_human_approval=True)
    assert res["decision"] == "BLOCKED"
