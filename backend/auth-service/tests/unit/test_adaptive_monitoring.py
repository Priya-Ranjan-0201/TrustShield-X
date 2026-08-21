import pytest
from app.services.adaptive_defense.adaptive_defense_fabric import AdaptiveDefenseFabric


def test_adaptive_monitoring_level_increase():
    fabric = AdaptiveDefenseFabric()
    rec = fabric.create_recommendation(
        tenant_id="tenant_mon",
        title="Increase audit and telemetry monitoring frequency on database server",
        action_classification="MONITORING_CHANGE",
        target_resource="srv-db-customer-records",
        automation_level="LEVEL_4_AUTOMATIC_SAFE_ACTION",
    )

    result = fabric.execute_closed_loop_defense(rec.recommendation_id)
    assert result["status"] == "COMPLETED"
    assert result["change"].action_type == "MONITORING_CHANGE"
