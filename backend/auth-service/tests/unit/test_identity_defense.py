import pytest
from app.services.adaptive_defense.adaptive_defense_fabric import AdaptiveDefenseFabric


def test_identity_defense_recommendation():
    fabric = AdaptiveDefenseFabric()
    rec = fabric.create_recommendation(
        tenant_id="tenant_idm",
        title="Require step-up MFA for anomalous service account session",
        action_classification="ACCESS_CHANGE",
        target_resource="svc_payment_batch_job",
        automation_level="LEVEL_3_PREAUTHORIZED_CONTROLLED_AUTOMATION",
    )

    result = fabric.execute_closed_loop_defense(rec.recommendation_id)
    assert result["status"] == "COMPLETED"
    assert result["verification"] == "VERIFIED"
