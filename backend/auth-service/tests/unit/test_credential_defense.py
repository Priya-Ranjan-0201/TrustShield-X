import pytest
from app.services.adaptive_defense.adaptive_defense_fabric import AdaptiveDefenseFabric


def test_credential_defense_workflow():
    fabric = AdaptiveDefenseFabric()
    rec = fabric.create_recommendation(
        tenant_id="tenant_cred",
        title="Invalidate active session tokens for leaked identity",
        action_classification="CREDENTIAL_CONTROL",
        target_resource="usr_session_compromised_token_99",
        automation_level="LEVEL_3_PREAUTHORIZED_CONTROLLED_AUTOMATION",
    )

    result = fabric.execute_closed_loop_defense(rec.recommendation_id)
    assert result["status"] == "COMPLETED"
    assert result["change"].action_type == "CREDENTIAL_CONTROL"
