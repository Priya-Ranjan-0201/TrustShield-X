import pytest
from app.services.adaptive_defense.adaptive_defense_fabric import AdaptiveDefenseFabric


def test_network_defense_closed_loop():
    fabric = AdaptiveDefenseFabric()
    rec = fabric.create_recommendation(
        tenant_id="tenant_net",
        title="Block egress to malicious C2 IP 198.51.100.33",
        action_classification="NETWORK_CONTROL",
        target_resource="198.51.100.33",
        automation_level="LEVEL_4_AUTOMATIC_SAFE_ACTION",
    )

    result = fabric.execute_closed_loop_defense(rec.recommendation_id)
    assert result["status"] == "COMPLETED"
    assert result["change"].action_type == "NETWORK_CONTROL"
    assert result["change"].target == "198.51.100.33"
