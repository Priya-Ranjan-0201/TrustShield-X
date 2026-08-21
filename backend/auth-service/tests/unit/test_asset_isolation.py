import pytest
from app.services.adaptive_defense.adaptive_defense_fabric import AdaptiveDefenseFabric


def test_asset_isolation_four_eyes_enforcement():
    fabric = AdaptiveDefenseFabric()
    rec = fabric.create_recommendation(
        tenant_id="tenant_ops",
        title="Isolate infected machine ep-finance-42",
        action_classification="ASSET_ISOLATION",
        target_resource="ep-finance-42",
        automation_level="LEVEL_2_HUMAN_APPROVAL",
    )

    # Execution blocked without approval
    res_blocked = fabric.execute_closed_loop_defense(rec.recommendation_id, has_human_approval=False)
    assert res_blocked["status"] == "APPROVAL_REQUIRED"

    # Execution proceeds with approval
    res_ok = fabric.execute_closed_loop_defense(rec.recommendation_id, has_human_approval=True)
    assert res_ok["status"] == "COMPLETED"
    assert res_ok["verification"] == "VERIFIED"
