import pytest
from app.services.adaptive_defense.adaptive_defense_fabric import AdaptiveDefenseFabric


def test_service_defense_requires_approval():
    fabric = AdaptiveDefenseFabric()
    rec = fabric.create_recommendation(
        tenant_id="tenant_svc",
        title="Temporarily restrict vulnerable feature endpoint",
        action_classification="SERVICE_CONTROL",
        target_resource="service-legacy-xml-parser",
        automation_level="LEVEL_2_HUMAN_APPROVAL",
    )

    res_no_app = fabric.execute_closed_loop_defense(rec.recommendation_id, has_human_approval=False)
    assert res_no_app["status"] == "APPROVAL_REQUIRED"
