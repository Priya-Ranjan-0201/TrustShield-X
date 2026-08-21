import pytest
from app.services.adaptive_defense.adaptive_defense_fabric import AdaptiveDefenseFabric


def test_defense_authorization_role_enforcement():
    fabric = AdaptiveDefenseFabric()
    rec = fabric.create_recommendation(
        tenant_id="tenant_auth",
        title="Isolate Node",
        action_classification="ASSET_ISOLATION",
        target_resource="ep-009",
        automation_level="LEVEL_2_HUMAN_APPROVAL",
    )

    decision = fabric.decision.evaluate_decision(rec, has_human_approval=False)
    assert decision.status == "APPROVAL_REQUIRED"
    assert decision.required_authorization == "FOUR_EYES_APPROVAL"
