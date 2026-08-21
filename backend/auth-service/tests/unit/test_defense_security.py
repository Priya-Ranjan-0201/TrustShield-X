import pytest
from app.services.adaptive_defense.adaptive_defense_fabric import AdaptiveDefenseFabric


def test_defense_security_blocks_protected_infrastructure():
    fabric = AdaptiveDefenseFabric()
    rec = fabric.create_recommendation(
        tenant_id="tenant_sec",
        title="Destroy localhost interface",
        action_classification="NETWORK_CONTROL",
        target_resource="127.0.0.1",
    )

    decision = fabric.decision.evaluate_decision(rec)
    assert decision.status == "BLOCKED"
    assert "protected infrastructure" in decision.explanation["why"].lower()
