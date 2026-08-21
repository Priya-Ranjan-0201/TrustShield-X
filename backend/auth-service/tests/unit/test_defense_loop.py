import pytest
from app.services.adaptive_defense.adaptive_defense_fabric import AdaptiveDefenseFabric


def test_closed_loop_defense_deduplication():
    fabric = AdaptiveDefenseFabric()
    rec = fabric.create_recommendation(
        tenant_id="tenant_loop",
        title="Block Scanner IP",
        action_classification="NETWORK_CONTROL",
        target_resource="198.51.100.12",
        automation_level="LEVEL_4_AUTOMATIC_SAFE_ACTION",
    )

    # First execution succeeds
    res1 = fabric.execute_closed_loop_defense(rec.recommendation_id)
    assert res1["status"] == "COMPLETED"

    # Repeated execution blocked by deduplication / cooldown
    res2 = fabric.execute_closed_loop_defense(rec.recommendation_id)
    assert res2["status"] == "BLOCKED"
    assert "blocked by circuit breaker" in res2["reason"]
